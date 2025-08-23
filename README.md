# LLM Batch Helper

[![PyPI version](https://badge.fury.io/py/llm_batch_helper.svg)](https://badge.fury.io/py/llm_batch_helper)
[![Downloads](https://pepy.tech/badge/llm_batch_helper)](https://pepy.tech/project/llm_batch_helper)
[![Downloads/Month](https://pepy.tech/badge/llm_batch_helper/month)](https://pepy.tech/project/llm_batch_helper)
[![Documentation Status](https://readthedocs.org/projects/llm-batch-helper/badge/?version=latest)](https://llm-batch-helper.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package that enables batch submission of prompts to LLM APIs, with built-in async capabilities, response caching, prompt verification, and more. This package is designed to streamline applications like LLM simulation, LLM-as-a-judge, and other batch processing scenarios.

📖 **[Complete Documentation](https://llm-batch-helper.readthedocs.io/)** | 🚀 **[Quick Start Guide](https://llm-batch-helper.readthedocs.io/en/latest/quickstart.html)**

## Why we designed this package

Calling LLM APIs has become increasingly common, but several pain points exist in practice:

1. **Efficient Batch Processing**: How do you run LLM calls in batches efficiently? Our async implementation is 3X-100X faster than multi-thread/multi-process approaches.

2. **API Reliability**: LLM APIs can be unstable, so we need robust retry mechanisms when calls get interrupted.

3. **Long-Running Simulations**: During long-running LLM simulations, computers can crash and APIs can fail. Can we cache LLM API calls to avoid repeating completed work?

4. **Output Validation**: LLM outputs often have format requirements. If the output isn't right, we need to retry with validation.

This package is designed to solve these exact pain points with async processing, intelligent caching, and comprehensive error handling. If there are some additional features you need, please post an issue.  

## Features

- **Async Processing**: Submit multiple prompts concurrently for faster processing
- **Response Caching**: Automatically cache responses to avoid redundant API calls
- **Multiple Input Formats**: Support for both file-based and list-based prompts
- **Provider Support**: Works with OpenAI (all models including GPT-5), OpenRouter (100+ models), and Together.ai APIs
- **Retry Logic**: Built-in retry mechanism with exponential backoff
- **Verification Callbacks**: Custom verification for response quality
- **Progress Tracking**: Real-time progress bars for batch operations

## Installation

### For Users (Recommended)

```bash
# Install from PyPI
pip install llm_batch_helper
```

### For Development

```bash
# Clone the repository
git clone https://github.com/TianyiPeng/LLM_batch_helper.git
cd llm_batch_helper

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Quick Start

### 1. Set up environment variables

**Option A: Environment Variables**
```bash
# For OpenAI (all models including GPT-5)
export OPENAI_API_KEY="your-openai-api-key"

# For OpenRouter (100+ models - Recommended)
export OPENROUTER_API_KEY="your-openrouter-api-key"

# For Together.ai
export TOGETHER_API_KEY="your-together-api-key"
```

**Option B: .env File (Recommended for Development)**
```python
# In your script, before importing llm_batch_helper
from dotenv import load_dotenv
load_dotenv()  # Load from .env file

# Then use the package normally
from llm_batch_helper import LLMConfig, process_prompts_batch
```

Create a `.env` file in your project:
```
OPENAI_API_KEY=your-openai-api-key
TOGETHER_API_KEY=your-together-api-key
```

### 2. Interactive Tutorial (Recommended)

Check out the comprehensive Jupyter notebook [tutorial](https://github.com/TianyiPeng/LLM_batch_helper/blob/main/tutorials/llm_batch_helper_tutorial.ipynb).

The tutorial covers all features with interactive examples!

### 3. Basic usage

```python
import asyncio
from dotenv import load_dotenv  # Optional: for .env file support
from llm_batch_helper import LLMConfig, process_prompts_batch

# Optional: Load environment variables from .env file
load_dotenv()

async def main():
    # Create configuration
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=100,  # or use max_tokens for backward compatibility
        max_concurrent_requests=30 # number of concurrent requests with asyncIO
    )
    
    # Process prompts
    prompts = [
        "What is the capital of France?",
        "What is 2+2?",
        "Who wrote 'Hamlet'?"
    ]
    
    results = await process_prompts_batch(
        config=config,
        provider="openai",
        prompts=prompts,
        cache_dir="cache"
    )
    
    # Print results
    for prompt_id, response in results.items():
        print(f"{prompt_id}: {response['response_text']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage Examples

### OpenRouter (Recommended - 100+ Models)

```python
import asyncio
from llm_batch_helper import LLMConfig, process_prompts_batch

async def openrouter_example():
    # Access 100+ models through OpenRouter
    config = LLMConfig(
        model_name="deepseek/deepseek-v3.1-base",  # or openai/gpt-4o, anthropic/claude-3-5-sonnet
        temperature=0.7,
        max_completion_tokens=500
    )
    
    prompts = [
        "Explain quantum computing briefly.",
        "What are the benefits of renewable energy?",
        "How does machine learning work?"
    ]
    
    results = await process_prompts_batch(
        prompts=prompts,
        config=config,
        provider="openrouter"  # Access to 100+ models!
    )
    
    for prompt_id, result in results.items():
        print(f"Response: {result['response_text']}")

if __name__ == "__main__":
    asyncio.run(openrouter_example())
```

### File-based Prompts

```python
import asyncio
from llm_batch_helper import LLMConfig, process_prompts_batch

async def process_files():
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=200
    )
    
    # Process all .txt files in a directory
    results = await process_prompts_batch(
        config=config,
        provider="openai",
        input_dir="prompts",  # Directory containing .txt files
        cache_dir="cache",
        force=False  # Use cached responses if available
    )
    
    return results

asyncio.run(process_files())
```

### Custom Verification

```python
from llm_batch_helper import LLMConfig

def verify_response(prompt_id, llm_response_data, original_prompt_text, **kwargs):
    """Custom verification callback"""
    response_text = llm_response_data.get("response_text", "")
    
    # Check minimum length
    if len(response_text) < kwargs.get("min_length", 10):
        return False
    
    # Check for specific keywords
    if "error" in response_text.lower():
        return False
    
    return True

config = LLMConfig(
    model_name="gpt-4o-mini",
    temperature=0.7,
    verification_callback=verify_response,
    verification_callback_args={"min_length": 20}
)
```



## API Reference

### LLMConfig

Configuration class for LLM requests.

```python
LLMConfig(
    model_name: str,
    temperature: float = 0.7,
    max_completion_tokens: Optional[int] = None,  # Preferred parameter
    max_tokens: Optional[int] = None,  # Deprecated, kept for backward compatibility
    system_instruction: Optional[str] = None,
    max_retries: int = 10,
    max_concurrent_requests: int = 5,
    verification_callback: Optional[Callable] = None,
    verification_callback_args: Optional[Dict] = None
)
```

### process_prompts_batch

Main function for batch processing of prompts.

```python
async def process_prompts_batch(
    config: LLMConfig,
    provider: str,  # "openai", "openrouter" (recommended), or "together"
    prompts: Optional[List[str]] = None,
    input_dir: Optional[str] = None,
    cache_dir: str = "llm_cache",
    force: bool = False,
    desc: str = "Processing prompts"
) -> Dict[str, Dict[str, Any]]
```

### LLMCache

Caching functionality for responses.

```python
cache = LLMCache(cache_dir="my_cache")

# Check for cached response
cached = cache.get_cached_response(prompt_id)

# Save response to cache
cache.save_response(prompt_id, prompt_text, response_data)

# Clear all cached responses
cache.clear_cache()
```

## Project Structure

```
llm_batch_helper/
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Locked dependencies
├── README.md                   # This file
├── LICENSE                     # License file
├── llm_batch_helper/          # Main package
│   ├── __init__.py            # Package exports
│   ├── cache.py               # Response caching
│   ├── config.py              # Configuration classes
│   ├── providers.py           # LLM provider implementations
│   ├── input_handlers.py      # Input processing utilities
│   └── exceptions.py          # Custom exceptions
├── examples/                   # Usage examples
│   ├── example.py             # Basic usage example
│   ├── prompts/               # Sample prompt files
│   └── llm_cache/             # Example cache directory
└── tutorials/                 # Interactive tutorials
    └── llm_batch_helper_tutorial.ipynb  # Comprehensive Jupyter notebook tutorial
```

## Supported Models

### OpenAI
- **All OpenAI models** 

### OpenRouter (Recommended - 100+ Models)
- **OpenAI models**: `openai/gpt-4o`, `openai/gpt-4o-mini`
- **Anthropic models**: `anthropic/claude-3-5-sonnet`, `anthropic/claude-3-haiku`
- **DeepSeek models**: `deepseek/deepseek-v3.1-base`, `deepseek/deepseek-chat`
- **Meta models**: `meta-llama/llama-3.1-405b-instruct`
- **Google models**: `google/gemini-pro-1.5`
- **And 90+ more models** from all major providers

### Together.ai
- meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
- meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
- mistralai/Mixtral-8x7B-Instruct-v0.1
- And many other open-source models

## Documentation

📖 **[Complete Documentation](https://llm-batch-helper.readthedocs.io/)** - Comprehensive docs on Read the Docs

### Quick Links:
- [Quick Start Guide](https://llm-batch-helper.readthedocs.io/en/latest/quickstart.html) - Get started quickly
- [API Reference](https://llm-batch-helper.readthedocs.io/en/latest/api.html) - Complete API documentation  
- [Examples](https://llm-batch-helper.readthedocs.io/en/latest/examples.html) - Practical usage examples
- [Tutorials](https://llm-batch-helper.readthedocs.io/en/latest/tutorials.html) - Step-by-step tutorials
- [Provider Guide](https://llm-batch-helper.readthedocs.io/en/latest/providers.html) - OpenAI, OpenRouter & Together.ai setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.5
- Added Together.ai provider support
- Support for open-source models (Llama, Mixtral, etc.)
- Enhanced documentation with Read the Docs
- Updated examples and tutorials

### v0.1.0
- Initial release
- Support for OpenAI API
- Async batch processing
- Response caching
- File and list-based input support
- Custom verification callbacks
- Poetry package management
