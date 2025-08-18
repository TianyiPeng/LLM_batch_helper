LLM Batch Helper Documentation
==============================

A Python package that enables batch submission of prompts to LLM APIs, with built-in async capabilities and response caching.

Features
--------

- **Async Processing**: Submit multiple prompts concurrently for faster processing
- **Response Caching**: Automatically cache responses to avoid redundant API calls
- **Multiple Input Formats**: Support for both file-based and list-based prompts
- **Provider Support**: Works with OpenAI and Together.ai APIs
- **Retry Logic**: Built-in retry mechanism with exponential backoff
- **Verification Callbacks**: Custom verification for response quality
- **Progress Tracking**: Real-time progress bars for batch operations

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

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def main():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=100
       )
       
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
       
       for prompt_id, response in results.items():
           print(f"{prompt_id}: {response['response_text']}")

   asyncio.run(main())

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`