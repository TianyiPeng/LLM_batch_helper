# LLM Batch Helper

[![PyPI version](https://badge.fury.io/py/llm_batch_helper.svg)](https://badge.fury.io/py/llm_batch_helper)
[![Downloads](https://pepy.tech/badge/llm_batch_helper)](https://pepy.tech/project/llm_batch_helper)
[![Downloads/Month](https://pepy.tech/badge/llm_batch_helper/month)](https://pepy.tech/project/llm_batch_helper)
[![Documentation Status](https://readthedocs.org/projects/llm-batch-helper/badge/?version=latest)](https://llm-batch-helper.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package that enables batch submission of prompts to LLM APIs, with built-in async capabilities, response caching, prompt verification, and more. This package is designed to streamline applications like LLM simulation, LLM-as-a-judge, and other batch processing scenarios.

📖 **[Complete Documentation](https://llm-batch-helper.readthedocs.io/)** | 🚀 **[Quick Start Guide](https://llm-batch-helper.readthedocs.io/en/latest/quickstart.html)**

## Why we designed this package

**Imagine you have 5000 prompts you need to send to an LLM. Running them sequentially can be painfully slow—sometimes taking hours or even days. Worse, if the process fails midway, you’re forced to start all over again.** We’ve struggled with this exact frustration, which is why we built this package, to directly tackle these pain points:

1. **Efficient Batch Processing**: How do you run LLM calls in batches efficiently? Our async implementation is 3X-100X faster than multi-thread/multi-process approaches. In my own experience, it reduces the time from 24 hours to 10min. 

2. **API Reliability**: LLM APIs can be unstable, so we need robust retry mechanisms when calls get interrupted.

3. **Long-Running Simulations**: During long-running LLM simulations, computers can crash and APIs can fail. Can we cache LLM API calls to avoid repeating completed work?

4. **Output Validation**: LLM outputs often have format requirements. If the output isn't right, we need to retry with validation.

This package is designed to solve these exact pain points with async processing, intelligent caching, and comprehensive error handling. If there are some additional features you need, please post an issue.  

## Features

- **🚀 Dramatic Speed Improvements**: **10-100x faster** than sequential processing ([see demo](https://github.com/TianyiPeng/LLM_batch_helper/blob/main/tutorials/performance_comparison_tutorial.ipynb))
- **⚡ Async Processing**: Submit multiple prompts concurrently for maximum throughput
- **💬 Message Mode**: **NEW!** Support for multi-turn conversations and conversation histories
- **💾 Smart Caching**: Automatically cache responses and resume interrupted work seamlessly
- **📝 Multiple Input Formats**: Support for strings, tuples, dictionaries, and file-based prompts
- **🌐 Multi-Provider Support**: Works with OpenAI (all models), OpenRouter (100+ models), Together.ai, and Google Gemini
- **🔄 Intelligent Retry Logic**: Built-in retry mechanism with exponential backoff and detailed logging
- **✅ Quality Control**: Custom verification callbacks for response validation
- **📊 Progress Tracking**: Real-time progress bars and comprehensive statistics
- **🎯 Simplified API**: No async/await complexity - works seamlessly in Jupyter notebooks (v0.3.0+)
- **🔧 Tunable Performance**: Adjust concurrency on-the-fly for optimal speed vs rate limits

## Installation

```bash
# Install from PyPI
pip install llm_batch_helper
```

## Quick Start

### 1. Set up environment variables

**Option A: Environment Variables**
```bash
# For OpenAI (all OpenAI models including GPT-5)
export OPENAI_API_KEY="your-openai-api-key"

# For OpenRouter (100+ models - Recommended)
export OPENROUTER_API_KEY="your-openrouter-api-key"

# For Together.ai
export TOGETHER_API_KEY="your-together-api-key"

# For Google Gemini
export GEMINI_API_KEY="your-gemini-api-key"
# OR alternatively:
export GOOGLE_API_KEY="your-gemini-api-key"
```

**Option B: .env File (Recommended for Development)**
Create a `.env` file in your project:
```
OPENAI_API_KEY=your-openai-api-key
```

```python
# In your script, before importing llm_batch_helper
from dotenv import load_dotenv
load_dotenv()  # Load from .env file

# Then use the package normally
from llm_batch_helper import LLMConfig, process_prompts_batch
```

### 2. Interactive Tutorials (Recommended)

**🎯 NEW: Performance Comparison Tutorial**
See the dramatic speed improvements! Our [Performance Comparison Tutorial](https://github.com/TianyiPeng/LLM_batch_helper/blob/main/tutorials/performance_comparison_tutorial.ipynb) demonstrates:
- **10-100x speedup** vs naive sequential processing
- Processing **5,000 prompts** in minutes instead of hours
- **Smart caching** that lets you resume interrupted work
- **Tunable concurrency** for optimal performance

**📚 Complete Feature Tutorial**
Check out the comprehensive [main tutorial](https://github.com/TianyiPeng/LLM_batch_helper/blob/main/tutorials/llm_batch_helper_tutorial.ipynb) covering all features with interactive examples!

### 3. Basic usage

```python
from dotenv import load_dotenv  # Optional: for .env file support
from llm_batch_helper import LLMConfig, process_prompts_batch

# Optional: Load environment variables from .env file
load_dotenv()

# Create configuration
config = LLMConfig(
    model_name="gpt-4o-mini",
    temperature=1.0,
    max_completion_tokens=100,
    max_concurrent_requests=100  # number of concurrent requests with asyncIO, this number decides how fast your pipeline can run. We suggest a number that is as large as possible (e.g., 300) while making sure you are not over the rate limit constrained by the LLM APIs. 
)

# Process prompts
prompts = [
    "What is the capital of France?",
    "What is 2+2?",
    "Who wrote 'Hamlet'?"
]

results = process_prompts_batch(
    config=config,
    provider="openai",
    prompts=prompts,
    cache_dir="cache"
)

# Print results
for prompt_id, response in results.items():
    print(f"{prompt_id}: {response['response_text']}")
```

**🎉 New in v0.3.0**: `process_prompts_batch` now handles async operations **implicitly** - no more async/await syntax needed! Works seamlessly in Jupyter notebooks.

### 4. Multiple Input Formats

The package supports three different input formats for maximum flexibility:

```python
from llm_batch_helper import LLMConfig, process_prompts_batch

config = LLMConfig(
    model_name="gpt-4o-mini",
    temperature=1.0,
    max_completion_tokens=100
)

# Mix different input formats in the same list
prompts = [
    # String format - ID will be auto-generated from hash
    "What is the capital of France?",
    
    # Tuple format - (custom_id, prompt_text)
    ("custom_id_1", "What is 2+2?"),
    
    # Dictionary format - {"id": custom_id, "text": prompt_text}
    {"id": "shakespeare_q", "text": "Who wrote 'Hamlet'?"},
    {"id": "science_q", "text": "Explain photosynthesis briefly."}
]

results = process_prompts_batch(
    config=config,
    provider="openai",
    prompts=prompts,
    cache_dir="cache"
)

# Print results with custom IDs
for prompt_id, response in results.items():
    print(f"{prompt_id}: {response['response_text']}")
```

**Input Format Requirements:**
- **String**: Plain text prompt (ID auto-generated)
- **Tuple**: `(prompt_id, prompt_text)` - both elements required
- **Dictionary**: `{"id": "prompt_id", "text": "prompt_text"}` - both keys required

### 💬 Message Mode (NEW!)

**New in v0.4.0**: Support for multi-turn conversations! You can now pass entire conversation histories directly to LLMs.

```python
from llm_batch_helper import LLMConfig, process_prompts_batch

config = LLMConfig(
    model_name="gpt-4o-mini",
    temperature=0.7,
    max_completion_tokens=200
)

# Message mode - pass conversation histories directly
messages = [
    # Multi-turn conversation
    ("conversation_1", [
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "What is 12 × 15?"},
        {"role": "assistant", "content": "12 × 15 = 180"},
        {"role": "user", "content": "How did you calculate that?"}
    ]),
    
    # Simple user message
    ("simple_question", [
        {"role": "user", "content": "Tell me a fun fact about space."}
    ]),
    
    # Dictionary format also supported
    {
        "id": "creative_task",
        "messages": [
            {"role": "system", "content": "You are a creative writing assistant."},
            {"role": "user", "content": "Write a haiku about programming."}
        ]
    }
]

results = process_prompts_batch(
    messages=messages,  # Use 'messages' instead of 'prompts'
    config=config,
    provider="openai"
)

for message_id, response in results.items():
    print(f"{message_id}: {response['response_text']}")
```

**Message Format Requirements:**
- **Tuple**: `(message_id, [{'role': 'user', 'content': '...'}])` - message list required
- **Dictionary**: `{"id": "message_id", "messages": [message_list]}` - both keys required
- **Roles**: Supports `"system"`, `"user"`, and `"assistant"` roles
- **Validation**: Only one of `prompts`, `messages`, or `input_dir` can be used at a time

**Key Benefits:**
- 🔄 **Multi-turn Support**: Pass entire conversation histories
- 🔧 **Full Compatibility**: Works with all providers and existing features (caching, retries, verification)
- 📈 **Same Performance**: Inherits all async and batching capabilities
- 🎯 **Flexible**: Mix different conversation lengths and formats in the same batch

**When to use each mode:**
- **Prompt Mode**: Single-turn interactions, simple Q&A, batch processing of independent prompts
- **Message Mode**: Multi-turn conversations, chat applications, when you need precise control over conversation context

### 🔄 Backward Compatibility

For users who prefer the async version or have existing code, the async API is still available:

```python
import asyncio
from llm_batch_helper import process_prompts_batch_async

async def main():
    results = await process_prompts_batch_async(
        prompts=["Hello world!"],
        config=config,
        provider="openai"
    )
    return results

results = asyncio.run(main())
```

## Usage Examples

### OpenRouter (Recommended - 100+ Models)

```python
from llm_batch_helper import LLMConfig, process_prompts_batch

# Access 100+ models through OpenRouter
config = LLMConfig(
    model_name="deepseek/deepseek-v3.1-base",  # or openai/gpt-4o, anthropic/claude-3-5-sonnet
    temperature=1.0,
    max_completion_tokens=500
)

prompts = [
    "Explain quantum computing briefly.",
    "What are the benefits of renewable energy?",
    "How does machine learning work?"
]

results = process_prompts_batch(
    prompts=prompts,
    config=config,
    provider="openrouter"  # Access to 100+ models!
)

for prompt_id, result in results.items():
    print(f"Response: {result['response_text']}")
```

### Google Gemini Provider

```python
from llm_batch_helper import LLMConfig, process_prompts_batch

config = LLMConfig(
    model_name="gemini-1.5-pro",  # or "gemini-1.5-flash"
    temperature=1.0,
    max_completion_tokens=200
)

prompts = [
    "Explain the theory of relativity.",
    "What are the main causes of climate change?",
    "How does photosynthesis work?"
]

results = process_prompts_batch(
    prompts=prompts,
    config=config,
    provider="gemini"  # Use Google Gemini!
)

for prompt_id, result in results.items():
    print(f"Response: {result['response_text']}")
```

### File-based Prompts

```python
from llm_batch_helper import LLMConfig, process_prompts_batch

config = LLMConfig(
    model_name="gpt-4o-mini",
    temperature=1.0,
    max_completion_tokens=200
)

# Process all .txt files in a directory
results = process_prompts_batch(
    config=config,
    provider="openai",
    input_dir="prompts",  # Directory containing .txt files
    cache_dir="cache",
    force=False  # Use cached responses if available
)

print(f"Processed {len(results)} prompts from files")
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
    temperature=1.0,
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
    temperature: float = 1.0,
    max_completion_tokens: Optional[int] = None,  # Preferred parameter
    max_tokens: Optional[int] = None,  # Deprecated, kept for backward compatibility
    system_instruction: Optional[str] = None,
    max_retries: int = 5,
    max_concurrent_requests: int = 30,
    verification_callback: Optional[Callable] = None,
    verification_callback_args: Optional[Dict] = None
)
```

### process_prompts_batch

Main function for batch processing of prompts (async operations handled implicitly).

```python
def process_prompts_batch(
    config: LLMConfig,
    provider: str,  # "openai", "openrouter" (recommended), or "together"
    prompts: Optional[List[str]] = None,
    input_dir: Optional[str] = None,
    cache_dir: str = "llm_cache",
    force: bool = False,
    desc: str = "Processing prompts"
) -> Dict[str, Dict[str, Any]]
```

### process_prompts_batch_async

Async version for backward compatibility and advanced use cases.

```python
async def process_prompts_batch_async(
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
    ├── llm_batch_helper_tutorial.ipynb  # Comprehensive feature tutorial
    └── performance_comparison_tutorial.ipynb  # Performance demo (NEW!)
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

### Google Gemini (Direct API)
- **gemini-1.5-pro**: Most capable model for complex reasoning tasks
- **gemini-1.5-flash**: Fast and cost-effective for most use cases
- **gemini-1.0-pro**: Previous generation model

**Note**: Gemini models support multimodal inputs (text, images, audio) through the Google AI Studio API.

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

### v0.3.3
- **🐛 Bug Fix**: Fixed caching issue that required verification_callback to be non-None
- **📦 Package Maintenance**: Version sync and build improvements
- Fixed version consistency across package files
- Updated build process for improved reliability

### v0.3.2
- **📚 Documentation Updates**: Enhanced README with performance focus
- Added new performance comparison tutorial showcasing 10-100x speedups
- Improved examples with simplified API usage (no async/await)
- Updated installation and quick start guides
- Enhanced content organization and clarity

### v0.3.1
- **🔧 Configuration Updates**: Optimized default values for better performance
- Updated `max_retries` from 10 to 5 for faster failure detection
- Updated `max_concurrent_requests` from 5 to 30 for improved batch processing performance

### v0.3.0
- **🎉 Major Update**: Simplified API - async operations handled implicitly, no async/await required!
- **📓 Jupyter Support**: Works seamlessly in notebooks without event loop issues
- **🔍 Detailed Retry Logging**: See exactly what happens during retries with timestamps
- **🔄 Backward Compatibility**: Original async API still available as `process_prompts_batch_async`
- **📚 Updated Examples**: All documentation updated to show simplified usage
- **⚡ Smart Event Loop Handling**: Automatically detects and handles different Python environments

### v0.2.0
- Enhanced API stability
- Improved error handling
- Better documentation

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
