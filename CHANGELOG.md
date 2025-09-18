# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-09-18

### Added
- **New Provider Support**: Google Gemini integration with direct API access
- Support for Gemini models: gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro
- Gemini-specific error handling for safety filter blocks
- Environment variable support for both GEMINI_API_KEY and GOOGLE_API_KEY
- Comprehensive Gemini documentation and examples in README
- Test script for validating Gemini provider functionality

### Changed
- Updated provider documentation to include Gemini across all examples
- Enhanced supported models section with Gemini model descriptions
- Added google-generativeai dependency to pyproject.toml

## [0.3.1] - 2025-09-06

### Changed
- Updated default `max_retries` parameter in `LLMConfig` from 10 to 5 for faster failure detection and improved user experience
- Updated default `max_concurrent_requests` parameter in `LLMConfig` from 5 to 30 for significantly improved batch processing performance

## [0.2.0] - 2025-01-15

### Added
- **New Provider Support**: OpenRouter integration for access to 100+ AI models
- Support for DeepSeek models (deepseek-chat, deepseek-v3.1-base) via OpenRouter
- Additional kwargs support in LLMConfig for provider-specific parameters
- Comprehensive OpenRouter documentation and examples

### Enhanced
- Provider system now supports OpenAI, Together.ai, and OpenRouter
- Updated documentation with OpenRouter setup instructions and model examples
- Enhanced provider comparison table including OpenRouter features

### Technical
- Added `_get_openrouter_response_direct` function with proper retry logic
- Extended provider dispatcher to handle OpenRouter API calls
- OpenRouter API endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Full compatibility with existing caching and verification systems

### Documentation
- Updated `docs/providers.rst` with OpenRouter configuration guide
- Added OpenRouter to README.md provider list
- Enhanced provider comparison with OpenRouter features and pricing model

## [0.1.4] - 2025-08-08

### Added
- Added `max_completion_tokens` parameter to `LLMConfig` for OpenAI API compatibility
- Backward compatibility support for legacy `max_tokens` parameter

### Changed
- Updated OpenAI API calls to use `max_completion_tokens` instead of deprecated `max_tokens`
- Relaxed httpx dependency constraint from `^0.24.0` to `>=0.24.0,<2.0.0` for better environment compatibility
- Updated README examples to use `max_completion_tokens`

### Fixed
- Automatic fallback when only `max_tokens` is provided to maintain backward compatibility

## [0.1.3] - 2025-08-08

### Added
- Initial backward compatibility improvements

## [0.1.2] - 2025-08-08

### Added
- Enhanced caching capabilities
- Tutorial improvements

## [0.1.1] - 2025-08-08

### Added
- Bug fixes and stability improvements

## [0.1.0] - 2025-08-08

### Added
- Initial release
- Support for OpenAI API
- Async batch processing with configurable concurrency
- Response caching system with automatic cache management
- File and list-based input support
- Custom verification callbacks for response quality control
- Retry logic with exponential backoff
- Progress tracking with real-time progress bars
- Poetry package management
- Comprehensive test suite
- Interactive Jupyter notebook tutorial

### Features
- **Async Processing**: Submit multiple prompts concurrently for faster processing
- **Response Caching**: Automatically cache responses to avoid redundant API calls
- **Multiple Input Formats**: Support for both file-based and list-based prompts
- **Provider Support**: Works with OpenAI API (gpt-4o-mini, gpt-4o, gpt-4, gpt-3.5-turbo)
- **Retry Logic**: Built-in retry mechanism with exponential backoff
- **Verification Callbacks**: Custom verification for response quality
- **Progress Tracking**: Real-time progress bars for batch operations