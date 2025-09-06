Changelog
=========

All notable changes to LLM Batch Helper will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[0.3.0] - 2025-01-XX
---------------------

Added
~~~~~
- **🎉 Simplified API**: ``process_prompts_batch()`` now works without async/await syntax!
- **📓 Jupyter Support**: Works seamlessly in notebooks without event loop management
- **🔍 Detailed Retry Logging**: See exactly what happens during retries with timestamps and error details
- **OpenRouter Provider**: Access to 100+ models through OpenRouter API (recommended)
- **Smart Event Loop Handling**: Automatically detects and handles different Python environments
- Support for ``nest_asyncio`` for improved Jupyter compatibility

Changed
~~~~~~~
- **Major API Update**: ``process_prompts_batch()`` is now the main synchronous interface
- **Default Temperature**: Changed from 0.7 to 1.0 to match OpenAI's defaults
- **Parameter Naming**: ``max_completion_tokens`` is now the preferred parameter over ``max_tokens``
- **Error Messages**: Enhanced error messages with retry attempt details
- **Documentation**: All examples updated to show simplified API usage

Fixed
~~~~~
- Jupyter notebook compatibility issues with asyncio event loops
- Improved error handling for authentication failures (401 errors)
- Better retry logic with exponential backoff logging

Backward Compatibility
~~~~~~~~~~~~~~~~~~~~~~
- Original async API still available as ``process_prompts_batch_async()``
- All existing code continues to work unchanged
- Legacy ``max_tokens`` parameter still supported

Migration Guide
~~~~~~~~~~~~~~~

**From v0.2.0 and earlier**:

.. code-block:: python

   # Old (still works)
   import asyncio
   results = await process_prompts_batch(...)
   
   # New (recommended)
   results = process_prompts_batch(...)  # No async/await needed!

[0.2.0] - 2024-XX-XX
---------------------

Changed
~~~~~~~
- Enhanced API stability
- Improved error handling
- Better documentation

[0.1.5] - 2024-08-17
---------------------

Added
~~~~~
- **Together.ai Provider Support**: Added support for Together.ai API as a new provider
- Support for various open-source models through Together.ai (Llama, Mixtral, etc.)
- Updated documentation to include Together.ai examples and configuration
- Added "together" keyword to package metadata

Changed
~~~~~~~
- Updated provider selection logic to support multiple providers
- Enhanced error handling for Together.ai specific errors
- Updated docstrings to reflect new provider options

Fixed
~~~~~
- Version synchronization between ``pyproject.toml`` and ``__init__.py``

[0.1.4] - 2024-01-XX
---------------------

Changed
~~~~~~~
- Relaxed httpx dependency version constraints for better compatibility
- Updated dependency management in ``pyproject.toml``

Fixed
~~~~~
- Dependency conflicts with other packages using httpx

[0.1.3] - 2024-01-XX
---------------------

Added
~~~~~
- Backward compatibility for ``max_tokens`` parameter (now ``max_completion_tokens``)
- Enhanced tutorial examples in Jupyter notebook

Changed
~~~~~~~
- Improved caching mechanism performance
- Better error messages for configuration issues

[0.1.2] - 2024-01-XX
---------------------

Fixed
~~~~~
- Cache directory creation issues on Windows
- Unicode handling in prompt files
- Progress bar display issues in certain terminal environments

[0.1.1] - 2024-01-XX
---------------------

Added
~~~~~
- Comprehensive Jupyter notebook tutorial
- Additional example scripts
- Better error handling for network issues

Changed
~~~~~~~
- Improved documentation structure
- Enhanced type hints throughout the codebase

[0.1.0] - 2024-01-XX
---------------------

Added
~~~~~
- Initial release of LLM Batch Helper
- **Core Features**:
  - Async batch processing of prompts
  - Response caching with automatic cache management
  - Support for OpenAI API (GPT models)
  - Multiple input formats (list-based and file-based)
  - Custom verification callbacks for response quality control
  - Built-in retry logic with exponential backoff
  - Progress tracking with real-time progress bars
  - Configurable concurrency control

- **API Components**:
  - ``LLMConfig`` class for configuration management
  - ``process_prompts_batch()`` main processing function
  - ``LLMCache`` for response caching
  - Input handlers for various prompt formats

- **Developer Tools**:
  - Poetry package management
  - Comprehensive test suite
  - Example scripts and tutorials
  - Type hints throughout

- **Documentation**:
  - Complete README with usage examples
  - API reference documentation
  - Jupyter notebook tutorial
  - Example scripts

Supported Models
~~~~~~~~~~~~~~~~

**OpenAI**:
- gpt-4o
- gpt-4o-mini  
- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo

**Together.ai** (Added in v0.1.5):
- meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
- meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
- mistralai/Mixtral-8x7B-Instruct-v0.1
- And many other open-source models

Migration Guide
---------------

From v0.1.4 to v0.1.5
~~~~~~~~~~~~~~~~~~~~~~

**New Together.ai Provider**:

.. code-block:: python

   # Old (OpenAI only)
   results = await process_prompts_batch(
       config=config,
       provider="openai",  # Only option
       prompts=prompts
   )

   # New (Multiple providers)
   results = await process_prompts_batch(
       config=config,
       provider="together",  # New option
       prompts=prompts
   )

**Environment Variables**:

.. code-block:: bash

   # Add Together.ai support
   export TOGETHER_API_KEY="your-together-key"

From v0.1.2 to v0.1.3
~~~~~~~~~~~~~~~~~~~~~~

**Token Parameter Update**:

.. code-block:: python

   # Old parameter name (still supported)
   config = LLMConfig(
       model_name="gpt-4o-mini",
       max_tokens=100  # Deprecated but works
   )

   # New parameter name (recommended)
   config = LLMConfig(
       model_name="gpt-4o-mini",
       max_completion_tokens=100  # Preferred
   )

Breaking Changes
----------------

None so far. The package maintains backward compatibility across all versions.

Known Issues
------------

- Rate limiting behavior may vary between OpenAI and Together.ai
- Some Together.ai models may have different response formats
- Very large batch sizes (>1000 prompts) may require memory optimization

Planned Features
----------------

- **v0.2.0**: Anthropic Claude API support
- **v0.2.1**: Google Gemini API support  
- **v0.3.0**: Streaming response support
- **v0.3.1**: Cost tracking and optimization features
- **v0.4.0**: Plugin architecture for custom providers