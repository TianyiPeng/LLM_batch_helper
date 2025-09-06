Quick Start Guide
=================

This guide will help you get started with LLM Batch Helper quickly.

🎉 **New in v0.3.0**: Simplified API - no more async/await syntax needed!

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install llm_batch_helper

Environment Setup
-----------------

Set up your API keys as environment variables:

.. code-block:: bash

   # For OpenAI (all models including GPT-5)
   export OPENAI_API_KEY="your-openai-api-key"
   
   # For OpenRouter (100+ models - Recommended)
   export OPENROUTER_API_KEY="your-openrouter-api-key"
   
   # For Together.ai
   export TOGETHER_API_KEY="your-together-api-key"

Or create a `.env` file in your project directory:

.. code-block:: text

   OPENAI_API_KEY=your-openai-api-key
   OPENROUTER_API_KEY=your-openrouter-api-key
   TOGETHER_API_KEY=your-together-api-key

Basic Usage
-----------

Simple Prompt Processing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   # Create configuration
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=1.0,
       max_completion_tokens=100,
       max_concurrent_requests=5
   )
   
   # Define prompts
   prompts = [
       "What is the capital of France?",
       "Explain quantum computing in simple terms.",
       "Write a haiku about programming."
   ]
   
   # Process prompts - no async/await needed!
   results = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,
       cache_dir="cache"
   )
   
   # Display results
   for prompt_id, response in results.items():
       print(f"Response {prompt_id}:")
       print(response['response_text'])
       print("-" * 50)

Using OpenRouter (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access 100+ models through OpenRouter:

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   config = LLMConfig(
       model_name="deepseek/deepseek-v3.1-base",  # or openai/gpt-4o, anthropic/claude-3-5-sonnet
       temperature=1.0,
       max_completion_tokens=150
   )
   
   prompts = [
       "Explain the benefits of renewable energy.",
       "What are the main programming paradigms?"
   ]
   
   results = process_prompts_batch(
       config=config,
       provider="openrouter",  # Access to 100+ models!
       prompts=prompts,
       cache_dir="openrouter_cache"
   )
   
   for prompt_id, response in results.items():
       print(f"{prompt_id}: {response['response_text']}")

Using Together.ai
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   config = LLMConfig(
       model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
       temperature=1.0,
       max_completion_tokens=150
   )
   
   prompts = [
       "Explain machine learning to a 10-year-old.",
       "What are the advantages of open-source software?"
   ]
   
   results = process_prompts_batch(
       config=config,
       provider="together",  # Use Together.ai
       prompts=prompts,
       cache_dir="together_cache"
   )
   
   for prompt_id, response in results.items():
       print(f"{prompt_id}: {response['response_text']}")

File-Based Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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
       input_dir="my_prompts",  # Directory with .txt files
       cache_dir="file_cache",
       force=False  # Use cached responses if available
   )
   
   print(f"Processed {len(results)} files!")

Configuration Options
---------------------

Key Parameters
~~~~~~~~~~~~~~

- ``model_name``: The LLM model to use (required)
- ``temperature``: Controls randomness (0.0 to 2.0, default: 1.0)
- ``max_completion_tokens``: Maximum tokens in the response (preferred)
- ``max_tokens``: Legacy parameter (use max_completion_tokens instead)
- ``max_concurrent_requests``: Number of parallel requests (default: 5)
- ``system_instruction``: System prompt for the model
- ``max_retries``: Number of retry attempts on failure (default: 10)
- ``verification_callback``: Custom function to verify response quality

Caching
~~~~~~~

Responses are automatically cached to avoid redundant API calls:

.. code-block:: python

   # First run - makes API calls
   results1 = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,
       cache_dir="my_cache"
   )
   
   # Second run - uses cached responses
   results2 = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,  # Same prompts
       cache_dir="my_cache",  # Same cache directory
       force=False  # Don't force regeneration
   )

Error Handling
~~~~~~~~~~~~~~

The package includes built-in retry logic with detailed logging and error handling:

.. code-block:: python

   config = LLMConfig(
       model_name="gpt-4o-mini",
       max_retries=5,  # Retry up to 5 times
       temperature=1.0
   )
   
   results = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts
   )
   
   # Check for errors in results
   for prompt_id, response in results.items():
       if "error" in response:
           print(f"Error in {prompt_id}: {response['error']}")
       else:
           print(f"Success: {response['response_text']}")

🔍 **New Retry Logging**: You'll see detailed logs during retries:

.. code-block:: text

   🔄 [14:23:15] Retry attempt 1/5:
      Error: RateLimitError (status: 429)
      Message: Rate limit exceeded...
      Waiting 4.0s before next attempt...

Next Steps
----------

- Check out the :doc:`api` reference for detailed documentation
- Explore :doc:`examples` for more complex use cases
- Learn about different :doc:`providers` and their features
- Try the interactive :doc:`tutorials`