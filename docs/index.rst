LLM Batch Helper Documentation
==============================

A Python package that enables batch submission of prompts to LLM APIs, with simplified interface and built-in async capabilities handled implicitly.

🎉 **New in v0.3.0**: Simplified API - no more async/await syntax needed!

Features
--------

- **Simplified API**: Async operations handled implicitly - no async/await needed
- **Jupyter Compatible**: Works seamlessly in notebooks without event loop issues
- **Response Caching**: Automatically cache responses to avoid redundant API calls
- **Multiple Input Formats**: Support for both file-based and list-based prompts
- **Provider Support**: Works with OpenAI (all models), OpenRouter (100+ models), and Together.ai APIs
- **Retry Logic**: Built-in retry mechanism with exponential backoff and detailed logging
- **Verification Callbacks**: Custom verification for response quality
- **Progress Tracking**: Real-time progress bars for batch operations
- **Detailed Error Logging**: See exactly what happens during retries with timestamps

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api
   providers
   examples
   tutorials
   changelog

Installation
============

.. code-block:: bash

   pip install llm_batch_helper

Quick Start
===========

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   # Create configuration
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=1.0,
       max_completion_tokens=100,
       max_concurrent_requests=100
   )
   
   # Define prompts
   prompts = [
       "What is the capital of France?",
       "What is 2+2?",
       "Who wrote 'Hamlet'?"
   ]
   
   # Process prompts - no async/await needed!
   results = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,
       cache_dir="cache"
   )
   
   # Print results
   for prompt_id, response in results.items():
       print(f"{prompt_id}: {response['response_text']}")

**🎉 New in v0.3.0**: No more async/await syntax needed! Works seamlessly in Jupyter notebooks.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`