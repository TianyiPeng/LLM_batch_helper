# LLM Batch Helper

A Python package that enables batch submission of prompts to LLM APIs, with built-in async capabilities and response caching.

## Features

- **Async Processing**: Submit multiple prompts concurrently for faster processing
- **Response Caching**: Automatically cache responses to avoid redundant API calls
- **Multiple Input Formats**: Support for both file-based and list-based prompts
- **Provider Support**: Works with OpenAI API
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

```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-api-key"
```

### 2. Interactive Tutorial (Recommended)

Check out the comprehensive Jupyter notebook [tutorial](https://github.com/TianyiPeng/LLM_batch_helper/blob/main/tutorials/llm_batch_helper_tutorial.ipynb).

The tutorial covers all features with interactive examples!

### 3. Basic usage

```python
import asyncio
from llm_batch_helper import LLMConfig, process_prompts_batch

async def main():
    # Create configuration
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_tokens=100,
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

### File-based Prompts

```python
import asyncio
from llm_batch_helper import LLMConfig, process_prompts_batch

async def process_files():
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_tokens=200
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
    max_tokens: Optional[int] = None,
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
    provider: str,  # "openai"
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
- gpt-4o-mini
- gpt-4o
- gpt-4
- gpt-3.5-turbo

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

### v0.1.0
- Initial release
- Support for OpenAI API
- Async batch processing
- Response caching
- File and list-based input support
- Custom verification callbacks
- Poetry package management
