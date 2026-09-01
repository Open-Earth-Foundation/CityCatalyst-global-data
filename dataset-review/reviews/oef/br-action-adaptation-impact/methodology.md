# Action-to-adaptation-risk methodology

> V1 is a proposed assessment awaiting human review. Indicator eligibility and the
> retained evidence have been conservatively reassessed. The current evidence review
> was completed locally without an external API; future model reruns use the same rules
> stored in the versioned prompts and runner.

## Purpose

The method connects adaptation actions to the vulnerability and exposure indicators in
the AdaptaBrasil risk framework. It records the evidence for each relationship and
produces component-level effectiveness claims. It does not calculate a city result or
an effect magnitude.

```text
Action
  -> indicator link claim
  -> direct links grouped by sector, risk and component
  -> evidence search for those direct links
  -> component effectiveness claim
  -> human review
```

## Indicator link claims

Every action is screened against every terminal indicator. The action is interpreted as
a whole before indicators are considered.

| Claim | Meaning | Eligible? |
| --- | --- | --- |
| `direct` | The action's primary mechanism directly changes the exact condition measured by the indicator. No unsupported intermediate assumption is required. | Yes |
| `indirect` | The indicator could change through a later effect, co-benefit or another intervention. | No |
| `no_link` | There is no credible relationship. | No |
| `unclear` | The supplied definitions do not establish whether the relationship is direct. | Human review |

Only direct claims proceed to evidence assessment. This prevents general resilience,
shared hazards and plausible co-benefits from inflating sector linkage counts.

The JSON stores direct, indirect and unclear claims. When indicator screening is marked
complete, an indicator absent from an action's claim list is an explicit `no_link`.
This avoids storing thousands of repetitive negative objects.

Exposure and vulnerability are assessed separately:

- Exposure requires a direct change to the exposed population, asset, area, activity or
  user quantity represented by the indicator.
- Vulnerability requires a direct change to the sensitivity, capacity, infrastructure,
  service, ecosystem, resource or other condition represented by the indicator.

Eligibility uses the action definition and risk framework. Evidence does not create or
broaden eligibility.

## Evidence

Evidence is searched for each action × sector × risk × component that contains at least
one direct indicator claim. A record contains:

- one source document and physical PDF page;
- one verbatim quotation;
- `supports`, `qualifies` or `contradicts`;
- `whole_action` or `partial_action` scope;
- the direct indicators addressed;
- any maladaptation signal;
- deterministic quote-grounding and human-review status.

The source registry appears once in the JSON. Evidence and screening records reference
it by `source_id`. Each evidence record belongs to exactly one sector-risk-component
group. The same passage may be retained for more than one risk only when it independently
supports each named risk; component claims reference those records by `evidence_id`.

The automated evidence stage uses local PDF text to retrieve candidate pages and asks
the model to assess only those supplied pages. Retrieval and the model prompt both use
the action, sector, risk, component and direct indicators. Every returned quote is
checked against its cited page, and it must also demonstrate the exact assessment
context. Quote grounding proves that words occur in a document; it does not by itself
prove that the passage is relevant. The retrieval method is recorded because a
candidate-page search is not equivalent to a human reading every page.

## Component effectiveness

Effectiveness is assessed for one action × sector × risk × component. Indicators
establish the direct relationship; they do not receive separate effectiveness ratings.

| Level | Rule |
| --- | --- |
| `High effectiveness` | The mechanism and indicator relationship are direct, and relevant evidence demonstrates a strong or quantified positive outcome. |
| `Medium effectiveness` | The mechanism and indicator relationship are direct, and relevant evidence demonstrates a moderate, conditional, context-dependent or mixed positive outcome. |
| `Low effectiveness` | The mechanism and indicator relationship are direct, and relevant evidence explicitly demonstrates a limited positive outcome. |
| `No demonstrated effectiveness` | No relevant positive evidence demonstrates one of the three effectiveness levels. This includes cases where evidence supports the direction of effect but not its strength. |

Scientific confidence is not outcome strength: wording such as “high confidence” does
not by itself justify High effectiveness. Low is never used for uncertainty, missing
quantification, partial document coverage or absence of evidence.

Source coverage is recorded separately as `none`, `single_source` or
`multiple_sources`. These values describe the evidence found; they are not scientific
confidence scores.

## Human review

Model-created claims and evidence begin as `proposed`. A person may accept, reject or
request correction. The review records the reviewer, date and note. A changed claim or
evidence record returns to proposed status.

The JSON is the assessment system of record. A spreadsheet may be generated from it for
review, but feedback must be applied back to the JSON-producing workflow rather than
creating a second calculation source.

## Implementation

The release has one runner, two prompts and one output:

- `releases/v1/run.py`
- `releases/v1/prompts/eligibility.md`
- `releases/v1/prompts/evidence.md`
- `releases/v1/output/action_risk_assessments.json`

Canonical inputs are actions, the risk framework, the source registry and source PDFs.
Extracted PDF text and model response checkpoints are disposable files under `.cache/`.
