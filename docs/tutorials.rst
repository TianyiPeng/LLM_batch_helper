Tutorials
=========

This section contains step-by-step tutorials to help you master LLM Batch Helper.

Interactive Jupyter Tutorial
-----------------------------

We provide a comprehensive Jupyter notebook tutorial that covers all features with interactive examples.

**Location:** ``tutorials/llm_batch_helper_tutorial.ipynb``

**How to Run:**

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/TianyiPeng/LLM_batch_helper.git
   cd llm_batch_helper

2. Install dependencies:

.. code-block:: bash

   poetry install

3. Start Jupyter:

.. code-block:: bash

   poetry run jupyter notebook tutorials/llm_batch_helper_tutorial.ipynb

**Tutorial Contents:**

- Basic setup and configuration
- Simple prompt processing
- File-based input handling
- Caching mechanisms
- Custom verification callbacks
- Error handling and retry logic
- Performance optimization
- Real-world use cases

Tutorial 1: Getting Started
----------------------------

This tutorial covers the absolute basics of using LLM Batch Helper.

Prerequisites
~~~~~~~~~~~~~

1. Python 3.11 or higher
2. An OpenAI API key or Together.ai API key
3. Basic knowledge of Python and async/await

Step 1: Installation and Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install the package
   pip install llm_batch_helper
   
   # Set up environment variables
   export OPENAI_API_KEY="your-key-here"

Step 2: Your First Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_step_2():
       # Create a simple configuration
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=50
       )
       
       # Define some simple prompts
       prompts = [
           "What is Python?",
           "What is machine learning?",
           "What is the capital of Japan?"
       ]
       
       # Process the prompts
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="tutorial_cache"
       )
       
       # Print results
       for i, (prompt_id, response) in enumerate(results.items()):
           print(f"Question {i+1}: {prompts[i]}")
           print(f"Answer: {response['response_text']}")
           print(f"Tokens used: {response['usage_details']['total_token_count']}")
           print("-" * 50)

   # Run the tutorial
   asyncio.run(tutorial_step_2())

Step 3: Understanding the Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The results dictionary contains detailed information for each prompt:

.. code-block:: python

   # Example result structure
   {
       "prompt_id_hash": {
           "response_text": "The actual LLM response",
           "usage_details": {
               "prompt_token_count": 15,
               "completion_token_count": 25,
               "total_token_count": 40
           }
       }
   }

Tutorial 2: Advanced Configuration
-----------------------------------

This tutorial covers advanced configuration options.

Step 1: Custom System Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_system_instructions():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.5,
           max_completion_tokens=100,
           system_instruction="""
           You are a helpful tutor specializing in computer science.
           Always provide clear, educational explanations suitable for beginners.
           Include practical examples when possible.
           """
       )
       
       prompts = [
           "What is a function in programming?",
           "Explain what a loop does.",
           "What is the difference between a list and a dictionary?"
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="tutorial_advanced_cache"
       )
       
       for prompt_id, response in results.items():
           print(response['response_text'])
           print("=" * 60)

   asyncio.run(tutorial_system_instructions())

Step 2: Concurrency Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_concurrency():
       # Test different concurrency levels
       prompts = [f"Tell me an interesting fact about number {i}" for i in range(1, 11)]
       
       configs = [
           LLMConfig(model_name="gpt-4o-mini", max_concurrent_requests=1),  # Sequential
           LLMConfig(model_name="gpt-4o-mini", max_concurrent_requests=5),  # Moderate
           LLMConfig(model_name="gpt-4o-mini", max_concurrent_requests=10), # High
       ]
       
       for i, config in enumerate(configs, 1):
           start_time = time.time()
           
           results = await process_prompts_batch(
               config=config,
               provider="openai",
               prompts=prompts,
               cache_dir=f"concurrency_test_{i}",
               desc=f"Concurrency test {config.max_concurrent_requests}"
           )
           
           end_time = time.time()
           duration = end_time - start_time
           
           print(f"Concurrency {config.max_concurrent_requests}: {duration:.2f} seconds")
           print(f"Processed {len(results)} prompts")
           print("-" * 40)

   asyncio.run(tutorial_concurrency())

Tutorial 3: File-Based Processing
----------------------------------

This tutorial shows how to process prompts from files.

Step 1: Prepare Your Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a directory structure:

.. code-block:: text

   my_prompts/
   ├── topic1.txt
   ├── topic2.txt
   └── topic3.txt

Each ``.txt`` file should contain one prompt.

Step 2: Process Files
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_file_processing():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.6,
           max_completion_tokens=200,
           system_instruction="Provide detailed, informative responses."
       )
       
       # Process all .txt files in the directory
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           input_dir="my_prompts",  # Directory with .txt files
           cache_dir="file_processing_cache",
           desc="Processing prompt files"
       )
       
       # Save results to individual files
       for prompt_id, response in results.items():
           output_filename = f"outputs/{prompt_id}_response.txt"
           with open(output_filename, 'w') as f:
               f.write(response['response_text'])
           print(f"Saved response to {output_filename}")

   asyncio.run(tutorial_file_processing())

Tutorial 4: Caching and Performance
------------------------------------

Understanding how caching works and optimizing performance.

Step 1: Cache Behavior
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import time
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_caching():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=100
       )
       
       prompts = [
           "What is artificial intelligence?",
           "Explain quantum computing.",
           "What is blockchain technology?"
       ]
       
       # First run - will make API calls
       print("First run (API calls):")
       start_time = time.time()
       
       results1 = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="caching_tutorial"
       )
       
       first_duration = time.time() - start_time
       print(f"Duration: {first_duration:.2f} seconds")
       
       # Second run - will use cache
       print("\nSecond run (cached):")
       start_time = time.time()
       
       results2 = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,  # Same prompts
           cache_dir="caching_tutorial"  # Same cache directory
       )
       
       second_duration = time.time() - start_time
       print(f"Duration: {second_duration:.2f} seconds")
       
       speedup = first_duration / second_duration
       print(f"Speedup: {speedup:.1f}x faster with cache")

   asyncio.run(tutorial_caching())

Step 2: Cache Management
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMCache

   # Create a cache instance
   cache = LLMCache("my_cache_directory")

   # Check if a specific response is cached
   prompt_id = "example_prompt_id"
   cached_response = cache.get_cached_response(prompt_id)

   if cached_response:
       print("Response found in cache")
   else:
       print("Response not in cache")

   # Clear all cached responses
   cache.clear_cache()
   print("Cache cleared")

Tutorial 5: Error Handling and Verification
--------------------------------------------

Building robust applications with proper error handling.

Step 1: Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def tutorial_error_handling():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=100,
           max_retries=3
       )
       
       # Include some problematic prompts
       prompts = [
           "Normal prompt",
           "",  # Empty prompt
           "Another normal prompt",
           "A" * 5000,  # Very long prompt
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="error_handling_tutorial"
       )
       
       # Check results and handle errors
       for prompt_id, response in results.items():
           if "error" in response:
               print(f"❌ Error in {prompt_id}: {response['error']}")
           else:
               print(f"✅ Success {prompt_id}: {len(response['response_text'])} chars")

   asyncio.run(tutorial_error_handling())

Step 2: Custom Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   def verify_python_code(prompt_id, llm_response_data, original_prompt_text, **kwargs):
       """Verify that the response contains valid Python code."""
       response_text = llm_response_data.get("response_text", "")
       
       # Simple checks for Python code
       python_keywords = ["def", "class", "import", "if", "for", "while"]
       has_python_keywords = any(keyword in response_text for keyword in python_keywords)
       
       # Check for code blocks
       has_code_block = "```" in response_text or "def " in response_text
       
       return has_python_keywords and has_code_block

   async def tutorial_verification():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.3,
           max_completion_tokens=300,
           system_instruction="Always provide working Python code examples.",
           verification_callback=verify_python_code,
           max_retries=3
       )
       
       prompts = [
           "Write a Python function to calculate the factorial of a number",
           "Create a Python class for a simple calculator",
           "Write Python code to read a CSV file"
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="verification_tutorial"
       )
       
       for prompt_id, response in results.items():
           if "error" in response:
               print(f"Verification failed: {response['error']}")
           else:
               print(f"✅ Verified Python code response")
               print(response['response_text'][:200] + "...")
               print("-" * 50)

   asyncio.run(tutorial_verification())

Next Steps
----------

After completing these tutorials, you should be comfortable with:

- Basic batch processing
- Advanced configuration options
- File-based input handling
- Caching for performance
- Error handling and verification
- Performance optimization

For more advanced usage patterns, check out the :doc:`examples` section or explore the complete :doc:`api` reference.