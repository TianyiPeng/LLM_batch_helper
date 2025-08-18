Quick Start Guide
=================

This guide will help you get started with LLM Batch Helper quickly.

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install llm_batch_helper

Environment Setup
-----------------

Set up your API keys as environment variables:

.. code-block:: bash

   # For OpenAI
   export OPENAI_API_KEY="your-openai-api-key"
   
   # For Together.ai
   export TOGETHER_API_KEY="your-together-api-key"

Or create a `.env` file in your project directory:

.. code-block:: text

   OPENAI_API_KEY=your-openai-api-key
   TOGETHER_API_KEY=your-together-api-key

Basic Usage
-----------

Simple Prompt Processing
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def basic_example():
       # Create configuration
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=100,
           max_concurrent_requests=5
       )
       
       # Define prompts
       prompts = [
           "What is the capital of France?",
           "Explain quantum computing in simple terms.",
           "Write a haiku about programming."
       ]
       
       # Process prompts
       results = await process_prompts_batch(
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

   # Run the example
   asyncio.run(basic_example())

Using Together.ai
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def together_example():
       config = LLMConfig(
           model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
           temperature=0.7,
           max_completion_tokens=150
       )
       
       prompts = [
           "Explain the benefits of renewable energy.",
           "What are the main programming paradigms?"
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="together",  # Use Together.ai
           prompts=prompts,
           cache_dir="together_cache"
       )
       
       for prompt_id, response in results.items():
           print(f"{prompt_id}: {response['response_text']}")

   asyncio.run(together_example())

File-Based Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def file_based_example():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=200
       )
       
       # Process all .txt files in a directory
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           input_dir="my_prompts",  # Directory with .txt files
           cache_dir="file_cache",
           force=False  # Use cached responses if available
       )
       
       return results

   results = asyncio.run(file_based_example())

Configuration Options
---------------------

Key Parameters
~~~~~~~~~~~~~~

- ``model_name``: The LLM model to use (required)
- ``temperature``: Controls randomness (0.0 to 2.0)
- ``max_completion_tokens``: Maximum tokens in the response
- ``max_concurrent_requests``: Number of parallel requests
- ``system_instruction``: System prompt for the model
- ``max_retries``: Number of retry attempts on failure

Caching
~~~~~~~

Responses are automatically cached to avoid redundant API calls:

.. code-block:: python

   # First run - makes API calls
   results1 = await process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,
       cache_dir="my_cache"
   )
   
   # Second run - uses cached responses
   results2 = await process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,  # Same prompts
       cache_dir="my_cache",  # Same cache directory
       force=False  # Don't force regeneration
   )

Error Handling
~~~~~~~~~~~~~~

The package includes built-in retry logic and error handling:

.. code-block:: python

   config = LLMConfig(
       model_name="gpt-4o-mini",
       max_retries=5,  # Retry up to 5 times
       temperature=0.7
   )
   
   results = await process_prompts_batch(
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

Next Steps
----------

- Check out the :doc:`api` reference for detailed documentation
- Explore :doc:`examples` for more complex use cases
- Learn about different :doc:`providers` and their features
- Try the interactive :doc:`tutorials`