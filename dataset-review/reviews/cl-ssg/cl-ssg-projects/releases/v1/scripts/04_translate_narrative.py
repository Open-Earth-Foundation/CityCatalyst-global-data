"""
Build a Spanish→English translation cache for the FICHA IDI corpus using OpenAI.

Inputs:
- CLI args:
  - ``--json-dir``: Directory of parsed FICHA IDI JSON files (default:
    ``corpus/parsed``).
  - ``--cache``: Output JSON cache path (default: ``data/derived/translations_es_en.json``).
  - ``--fields``: Optional list of ``TRANSLATABLE_FIELDS`` CSV column names to scan.
  - ``--limit``: Translate at most N new strings for smoke tests.
  - ``--save-every``: Save after N completed translations (default: 200).
  - ``--model``: OpenAI model to use (default: ``gpt-4o-mini``; use ``gpt-4o``
    for higher quality on long fields).
  - ``--batch-size``: Number of strings per OpenAI request (default: 10).
  - ``--concurrency``: Number of concurrent OpenAI batches (default: 8).
- Files/paths: ``--json-dir`` should contain parsed ``*.json`` files with FICHA
  IDI fields; ``--cache`` is a flat ``{spanish: english}`` JSON object.
- Env vars: ``OPENAI_API_KEY`` is required for the official OpenAI Python SDK.

Outputs:
- Writes the translation cache as UTF-8 JSON using the existing atomic
  ``.tmp`` + replace save pattern.
- Prints progress, rough cost estimates, and validation failures to stdout/stderr.

Usage (from this release directory):
- ``python scripts/04_translate_narrative.py --limit 50``
- ``python scripts/04_translate_narrative.py``

The cache is consumed by ``scripts/03_add_english_columns.py --translations-cache <path>``
to add ``_en`` columns alongside each ``_es`` column (written to
``data/derived/ficha_idi_table_translated.csv`` by default).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import signal
import sys
import time
from pathlib import Path
from typing import Any

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "derived"
CORPUS = ROOT / "corpus"
DEFAULT_JSON_DIR = CORPUS / "parsed"
DEFAULT_CACHE = DERIVED / "translations_es_en.json"

# JSON paths mapped to the column name we use in the English CSV.
# (path, csv_column_name)
TRANSLATABLE_FIELDS = [
    (("etapas", "*", "narrative", "justificacion"),                                "justification_es"),
    (("etapas", "*", "narrative", "descripcion_etapa"),                            "description_es"),
    (("etapas", "*", "resumen_resultados", "indicadores", "proposito"),            "purpose_es"),
    (("etapas", "*", "resumen_resultados", "indicadores", "indicadores_proposito"), "purpose_indicators_es"),
    (("etapas", "*", "resumen_resultados", "indicadores", "componentes"),          "components_es"),
    (("etapas", "*", "resumen_resultados", "indicadores", "indicadores_componentes"), "component_indicators_es"),
    (("etapas", "*", "conclusiones_analisis"),                                     "conclusions_es"),
    (("etapas", "*", "clasificacion", "sector_subsector_raw"),                     "sector_subsector_raw_es"),
    (("etapas", "*", "ubicacion", "raw"),                                          "location_raw_es"),
]


# ---------------------------------------------------------------------------
# Walk JSON to collect unique strings
# ---------------------------------------------------------------------------

def walk(obj, path):
    """Yield values matching the path, where '*' is a wildcard for list indexing."""
    if not path:
        if isinstance(obj, list):
            yield from obj
        else:
            yield obj
        return
    head, *rest = path
    if head == "*":
        if isinstance(obj, list):
            for x in obj:
                yield from walk(x, rest)
    else:
        if isinstance(obj, dict) and head in obj:
            yield from walk(obj[head], rest)


def collect_unique_strings(json_dir: Path, fields: list[str]) -> set[str]:
    seen: set[str] = set()
    selected_paths = [(p, name) for (p, name) in TRANSLATABLE_FIELDS if name in fields]
    for fp in sorted(json_dir.glob("*.json")):
        try:
            d = json.loads(fp.read_text())
        except Exception:
            continue
        for path, _name in selected_paths:
            for v in walk(d, list(path)):
                if isinstance(v, str):
                    s = v.strip()
                    if s:
                        seen.add(s)
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, str) and x.strip():
                            seen.add(x.strip())
    return seen


# ---------------------------------------------------------------------------
# Translation backend (OpenAI)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You translate Chilean public-sector project documents (FICHA IDI / SNI), including technical and governmental Spanish.

Translate Spanish to English faithfully and concisely. Do not paraphrase. Do not add commentary, preambles, labels, notes, or explanations.

Preserve verbatim: numbers, percentages, currency, dates, formulas like (N°X / Y) * 100, proper nouns, and acronyms such as FNDR, MINVU, MOP, MIDESO, RSD, APR, APL, ESSBIO, INDAP, CONAF, PYME, IDI. Keep acronyms uppercase. If an acronym is obscure, you may add a brief English gloss in parentheses on first occurrence.

Normalize ALL CAPS Spanish input to sentence case before translating. Output must use natural English capitalization, never ALL CAPS.

Preserve the list, bullet, and sentence structure of the source, including newlines, dashes, and semicolons.

If a term is ambiguous or genuinely untranslatable, leave the Spanish word in [square brackets] rather than guessing.

Output only the requested translation text. For batched requests, return only the requested JSON object.
"""

TOKEN_REPETITION_RE = re.compile(r"(?i)(?:^|\s)(\S+)(?:\s+\1){3,}(?=\s|$)")
MIN_LENGTH_RATIO = 0.3
MAX_LENGTH_RATIO = 3.0
SOLO_CHAR_LIMIT = 8000
MINI_INPUT_PER_1M = 0.150
MINI_OUTPUT_PER_1M = 0.600
TOKEN_PER_CHAR = 0.4


def validate_translation(source: str, translation: str) -> list[str]:
    """Return validation failure messages for one translated string."""
    failures: list[str] = []
    if not translation.strip():
        failures.append("empty output")
        return failures

    ratio = len(translation) / max(len(source), 1)
    if ratio < MIN_LENGTH_RATIO or ratio > MAX_LENGTH_RATIO:
        failures.append(f"length ratio {ratio:.2f} outside {MIN_LENGTH_RATIO}-{MAX_LENGTH_RATIO}")
    if TOKEN_REPETITION_RE.search(translation):
        failures.append("single token repeated 4+ times in a row")
    return failures


def estimate_mini_cost(strings: list[str]) -> tuple[float, float, float]:
    """Estimate gpt-4o-mini input/output cost from Spanish character counts."""
    estimated_tokens = sum(len(s) for s in strings) * TOKEN_PER_CHAR
    input_cost = estimated_tokens / 1_000_000 * MINI_INPUT_PER_1M
    output_cost = estimated_tokens / 1_000_000 * MINI_OUTPUT_PER_1M
    return input_cost, output_cost, input_cost + output_cost


def chunk_todo(strings: list[str], batch_size: int) -> list[list[str]]:
    """Group strings into OpenAI batches, keeping very long strings solo."""
    batches: list[list[str]] = []
    current: list[str] = []
    for s in strings:
        if len(s) > SOLO_CHAR_LIMIT:
            if current:
                batches.append(current)
                current = []
            batches.append([s])
            continue
        current.append(s)
        if len(current) >= batch_size:
            batches.append(current)
            current = []
    if current:
        batches.append(current)
    return batches


async def request_translations(
    client: Any,
    model: str,
    texts: list[str],
    temperature: float,
) -> dict[int, str]:
    """Request translations for one batch and return them keyed by batch id."""
    payload = [{"id": i, "text": text} for i, text in enumerate(texts)]
    user_prompt = (
        "Translate each Spanish text in this JSON array to English. Return exactly "
        '{"translations": [{"id": int, "translation": str}, ...]} with one '
        "translation for every input id and no extra keys.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )
    response = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response")

    data = json.loads(content)
    translations = data.get("translations")
    if not isinstance(translations, list):
        raise ValueError("OpenAI response missing translations array")

    out: dict[int, str] = {}
    for item in translations:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        translation = item.get("translation")
        if isinstance(item_id, int) and isinstance(translation, str):
            out[item_id] = translation.strip()
    return out


async def translate_one_with_retries(
    client: Any,
    model: str,
    source: str,
    reason: str,
) -> str:
    """Translate one string solo, retrying validation failures with higher temperature."""
    last_failure = reason
    for attempt, temperature in enumerate((0.2, 0.4), 1):
        try:
            translated = (await request_translations(client, model, [source], temperature)).get(0, "")
            failures = validate_translation(source, translated)
            if not failures:
                return translated
            last_failure = "; ".join(failures)
        except Exception as e:
            last_failure = str(e)
        sys.stderr.write(
            f"  solo retry {attempt}/2 failed for {len(source)}-char string: {last_failure}\n"
        )

    sys.stderr.write(
        f"  translate FAILED after retries for {len(source)}-char string: {last_failure}\n"
    )
    return f"[UNTRANSLATED] {source}"


async def process_batch(
    client: Any,
    model: str,
    batch: list[str],
    semaphore: asyncio.Semaphore,
) -> dict[str, str]:
    """Translate one batch, retrying invalid or missing items solo."""
    async with semaphore:
        try:
            batch_translations = await request_translations(client, model, batch, temperature=0.0)
        except Exception as e:
            sys.stderr.write(
                f"  batch FAILED for {len(batch)} strings; retrying solo: {e}\n"
            )
            return {
                source: await translate_one_with_retries(client, model, source, str(e))
                for source in batch
            }

        results: dict[str, str] = {}
        for i, source in enumerate(batch):
            translated = batch_translations.get(i, "")
            failures = validate_translation(source, translated)
            if failures:
                results[source] = await translate_one_with_retries(
                    client,
                    model,
                    source,
                    "; ".join(failures),
                )
            else:
                results[source] = translated
        return results


# ---------------------------------------------------------------------------
# Cache I/O with periodic saves and graceful interrupt
# ---------------------------------------------------------------------------

def load_cache(p: Path) -> dict[str, str]:
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def save_cache(p: Path, cache: dict[str, str]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True))
    tmp.replace(p)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the translation cache builder."""
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR,
                    help=f"Directory of parsed FICHA IDI JSON files (default: {DEFAULT_JSON_DIR})")
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE,
                    help=f"Translation cache file (default: {DEFAULT_CACHE})")
    ap.add_argument("--fields", nargs="+",
                    default=[name for (_p, name) in TRANSLATABLE_FIELDS],
                    help="Restrict to these CSV column names. Default: all 9 _es fields.")
    ap.add_argument("--limit", type=int, default=None,
                    help="Translate at most N new strings (smoke test).")
    ap.add_argument("--save-every", type=int, default=200,
                    help="Save cache every N translations (default 200).")
    ap.add_argument("--model", default="gpt-4o-mini",
                    help="OpenAI model to use (default: gpt-4o-mini; use gpt-4o for long fields).")
    ap.add_argument("--batch-size", type=int, default=10,
                    help="Strings per OpenAI request; >8000-char strings are translated solo (default 10).")
    ap.add_argument("--concurrency", type=int, default=8,
                    help="Concurrent OpenAI batches (default 8).")
    return ap.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def run(args: argparse.Namespace) -> int:
    """Run the async OpenAI translation workflow and persist the cache."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable is required.", file=sys.stderr)
        return 1

    if AsyncOpenAI is None:
        print(
            "ERROR: openai Python SDK is not installed. Install with: pip install openai",
            file=sys.stderr,
        )
        return 1

    if args.batch_size < 1:
        print("ERROR: --batch-size must be >= 1", file=sys.stderr)
        return 1
    if args.concurrency < 1:
        print("ERROR: --concurrency must be >= 1", file=sys.stderr)
        return 1
    if args.save_every < 1:
        print("ERROR: --save-every must be >= 1", file=sys.stderr)
        return 1

    if not args.json_dir.exists():
        print(f"ERROR: json dir not found: {args.json_dir}", file=sys.stderr)
        return 1

    print(f"Scanning {args.json_dir} for unique Spanish strings in {len(args.fields)} fields…")
    uniques = collect_unique_strings(args.json_dir, args.fields)
    print(f"Found {len(uniques):,} unique strings.")

    cache = load_cache(args.cache)
    print(f"Cache currently has {len(cache):,} translations at {args.cache}")

    todo = sorted(s for s in uniques if s not in cache)
    if args.limit is not None:
        todo = todo[:args.limit]
    print(f"To translate this run: {len(todo):,}")
    if not todo:
        print("Nothing to do — cache is fully populated for these fields.")
        return 0

    input_cost, output_cost, total_cost = estimate_mini_cost(todo)
    print(
        "Estimated cost at gpt-4o-mini pricing "
        f"(${MINI_INPUT_PER_1M:.3f}/1M input, ${MINI_OUTPUT_PER_1M:.3f}/1M output): "
        f"input=${input_cost:.4f} output=${output_cost:.4f} total=${total_cost:.4f}"
    )
    print(
        f"Using OpenAI model={args.model} batch_size={args.batch_size} "
        f"concurrency={args.concurrency}"
    )

    # Graceful interrupt: save cache on SIGINT.
    interrupted = {"flag": False}
    def _on_int(signum, frame):
        interrupted["flag"] = True
        print("\nInterrupt received — saving cache then exiting…")
        save_cache(args.cache, cache)
    signal.signal(signal.SIGINT, _on_int)

    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    batches = chunk_todo(todo, args.batch_size)
    semaphore = asyncio.Semaphore(args.concurrency)
    total_chars = sum(len(s) for s in todo)
    t0 = time.time()
    chars_done = 0
    done = 0
    saved_at = 0

    for offset in range(0, len(batches), args.concurrency):
        if interrupted["flag"]:
            break
        wave = batches[offset:offset + args.concurrency]
        wave_results = await asyncio.gather(
            *(process_batch(client, args.model, batch, semaphore) for batch in wave)
        )

        for result in wave_results:
            if interrupted["flag"]:
                break
            cache.update(result)
            batch_chars = sum(len(s) for s in result)
            chars_done += batch_chars
            done += len(result)

            if done - saved_at >= args.save_every:
                save_cache(args.cache, cache)
                saved_at = done

            elapsed = time.time() - t0
            rate = chars_done / max(elapsed, 0.001)
            remaining = max(total_chars - chars_done, 0)
            eta_sec = remaining / max(rate, 0.001)
            print(
                f"[{done}/{len(todo)}] cache={len(cache):,} "
                f"chars={chars_done/1e6:.2f}Mchars rate={rate:.0f}cps "
                f"ETA={eta_sec/60:.0f}min"
            )

        if interrupted["flag"]:
            save_cache(args.cache, cache)
            break

    save_cache(args.cache, cache)
    elapsed = time.time() - t0
    print(f"\nDone. {len(cache):,} total translations in cache.")
    print(f"This run translated {chars_done:,} characters in {elapsed/60:.1f} min.")
    print(f"Cache file: {args.cache}")
    return 0 if not interrupted["flag"] else 130


def main() -> int:
    """Parse args and run the translation cache builder."""
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    sys.exit(main())
