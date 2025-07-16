# LLM Batch Helper Examples

This directory contains examples of how to use the `llm_batch_helper` package.

## Directory Structure

```
text_simulation/
├── llm_batch_helper/           # The package
│   ├── __init__.py
│   ├── config.py
│   ├── providers.py
│   └── cache.py
└── llm_batch_helper_examples/  # Examples
    ├── README.md
    ├── example_with_files.py
    ├── prompts/               # Input prompt files
    │   ├── france.txt
    │   ├── math.txt
    │   └── shakespeare.txt
    └── cache/                # Cached responses
        ├── france.json
        ├── math.json
        └── shakespeare.json
```

## Running the Examples

1. Make sure you have set up your environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. Run the example:
   ```bash
   cd llm_batch_helper_examples
   python example_with_files.py
   ```

## How It Works

1. The example creates a `prompts` directory with sample text files
2. Each text file contains a prompt for the LLM
3. The script processes all prompts and saves responses in the `cache` directory
4. Each cached response is saved as a JSON file with the same name as the input file

## Customizing

To use your own prompts:

1. Create text files in the `prompts` directory
2. Each file should contain a single prompt
3. The filename (without extension) will be used as the prompt ID
4. Run the script to process your prompts

To force regeneration of responses:
```python
await process_input_folder(
    input_dir="your_input_dir",
    cache_dir="your_cache_dir",
    force=True  # Force regeneration
)
``` 