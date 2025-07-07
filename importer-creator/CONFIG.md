# Configuration Guide

## Overview

The importer-creator now uses a **simple BIG_MODEL/SMALL_MODEL convention** with OpenRouter support, allowing easy model switching and cost optimization.

## Configuration File

### Location

- `config.yaml` in the root of the importer-creator directory

### Simple Model Configuration

```yaml
models:
  # Simple two-model approach
  BIG_MODEL: "openai/gpt-4o" # For complex data analysis, coding, transformations
  SMALL_MODEL: "openai/gpt-4o-mini" # For structured output parsing, simple tasks
  EMBEDDINGS_MODEL: "text-embedding-3-large"
```

**That's it!** No complex mappings or assignments needed.

### How Models Are Used

- **BIG_MODEL**: Used by `create_coding_agent()` for complex pandas operations, data analysis, and transformations
- **SMALL_MODEL**: Used by `llm_with_structured_output()` for JSON parsing and simple formatting tasks
- **EMBEDDINGS_MODEL**: Used for vector store operations

### Changing Models

Simply update the model names in `config.yaml`:

```yaml
BIG_MODEL: "anthropic/claude-sonnet-4" # Switch to Claude for complex tasks
SMALL_MODEL: "google/gemini-2.5-flash" # Switch to flash for simplie
```

**Popular OpenRouter Models:**

- `anthropic/claude-4,0-sonnet` - Excellent reasoning
- `google/gemini-2.5-flash` - Fast and capable
- `meta-llama/llama-3.2-70b-instruct` - Open source option
- `deepseek/deepseek-r1-0528` - Great for reasoning tasks

## Code Usage

### In Your Code

```python
from utils.config_loader import ConfigLoader

# Get models directly
big_model = ConfigLoader.get_big_model()
small_model = ConfigLoader.get_small_model()

# Agent creation automatically uses the right models
coding_agent = AgentFactory.get_coding_agent(df, verbose)        # Uses BIG_MODEL
structured_agent = AgentFactory.get_structured_output_agent(verbose)  # Uses SMALL_MODEL
```

### Clear Model Assignment

- **Complex Tasks → BIG_MODEL**: Data analysis, pandas operations, complex reasoning
- **Simple Tasks → SMALL_MODEL**: JSON parsing, structured output, formatting

## Environment Setup

### 1. Get OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Create an account and generate an API key
3. Copy your API key (starts with `sk-or-...`)

### 2. Set Environment Variable

**Option A: Update `.env` file**

```bash
OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

**Option B: Command line (Windows)**

```cmd
set OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

**Option C: Command line (Mac/Linux)**

```bash
export OPENROUTER_API_KEY=sk-or-your-actual-api-key-here
```

## Cost Optimization

### Model Selection Strategy

1. **BIG_MODEL (Complex Tasks)**

   - Use for data analysis, transformations, complex reasoning
   - Recommended: `openai/gpt-4o` or `anthropic/claude-3.5-sonnet`
   - Higher cost but better accuracy for complex tasks

2. **SMALL_MODEL (Simple Tasks)**

   - Use for JSON parsing, structured output, simple formatting
   - Recommended: `openai/gpt-4o-mini` or `anthropic/claude-3-haiku`
   - Lower cost, sufficient for structured parsing

### Example Cost-Optimized Configuration

```yaml
models:
  BIG_MODEL: "openai/gpt-4o" # $2.50/$10.00 per 1M tokens
  SMALL_MODEL: "openai/gpt-4o-mini" # $0.15/$0.60 per 1M tokens
  EMBEDDINGS_MODEL: "text-embedding-3-large" # $0.13 per 1M tokens
```

### Budget-Friendly Option

```yaml
models:
  BIG_MODEL: "openai/gpt-4o-mini" # Use mini for everything
  SMALL_MODEL: "openai/gpt-4o-mini" # Same model, very low cost
```

### Performance-Optimized Option

```yaml
models:
  BIG_MODEL: "anthropic/claude-3.5-sonnet" # Best reasoning
  SMALL_MODEL: "anthropic/claude-3-haiku" # Fast parsing
```

## Advanced Configuration

### Rate Limiting & Retries

```yaml
api:
  timeout: 60
  max_retries: 3
```

### Site Attribution (Optional)

```yaml
headers:
  http_referer: "Your-Site-URL"
  x_title: "Your Application Name"
```

## Troubleshooting

### Common Issues

1. **"OPENROUTER_API_KEY environment variable not set"**

   - Solution: Set the environment variable as shown above

2. **Model not found errors**

   - Check [OpenRouter Models](https://openrouter.ai/models) for available models
   - Ensure model name is exactly as listed (case-sensitive)

3. **Rate limiting errors**

   - Increase timeout in `config.yaml`
   - Consider using models with higher rate limits
   - Add delays between requests if needed

4. **Cost concerns**

   - Monitor usage at [OpenRouter Dashboard](https://openrouter.ai/activity)
   - Switch to cheaper models for non-critical tasks
   - Use the `:free` variant for testing: `openai/gpt-4o-mini:free`

## Benefits of This Approach

### ✅ **Simple & Clear**

- Only **2 models** to configure: BIG_MODEL and SMALL_MODEL
- **No complex mappings** or assignments
- **Direct usage** in code: `get_big_model()` and `get_small_model()`

### ✅ **Cost Effective**

- **Automatic optimization**: Expensive models only for complex tasks
- **Easy cost control**: Change one line to switch all complex tasks
- **Clear cost allocation**: Know exactly what each model is used for

### ✅ **Flexible**

- **Easy experimentation**: Try different models with single config change
- **Provider diversity**: Access 200+ models via OpenRouter
- **Automatic fallbacks**: OpenRouter handles provider outages

## Quick Start

1. **Set API key**: `OPENROUTER_API_KEY=sk-or-your-key`
2. **Choose models**: Edit `BIG_MODEL` and `SMALL_MODEL` in `config.yaml`
3. **Run**: The system automatically uses the right model for each task

That's it! 🚀
