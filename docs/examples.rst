Examples
========

This page contains practical examples demonstrating various features of LLM Batch Helper.

Basic Examples
--------------

Simple Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def simple_batch():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=100
       )
       
       prompts = [
           "What is machine learning?",
           "Explain neural networks briefly.",
           "What is deep learning?"
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=prompts,
           cache_dir="ml_cache"
       )
       
       for prompt_id, response in results.items():
           print(f"Q: {prompts[int(prompt_id.split('_')[-1])]}")
           print(f"A: {response['response_text']}\n")

   asyncio.run(simple_batch())

File-Based Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def process_files():
       """Process all .txt files in a directory."""
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.5,
           max_completion_tokens=300,
           system_instruction="You are a helpful assistant providing detailed explanations."
       )
       
       # Process all .txt files in the 'questions' directory
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           input_dir="questions",  # Directory containing .txt files
           cache_dir="answers_cache",
           desc="Processing question files"
       )
       
       # Save results to files
       for prompt_id, response in results.items():
           if "error" not in response:
               with open(f"answers/{prompt_id}_answer.txt", "w") as f:
                   f.write(response['response_text'])

   asyncio.run(process_files())

Advanced Examples
-----------------

Custom Verification
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   def verify_code_response(prompt_id, llm_response_data, original_prompt_text, **kwargs):
       """Verify that code responses contain actual code."""
       response_text = llm_response_data.get("response_text", "")
       
       # Check for code indicators
       code_indicators = ["def ", "class ", "import ", "```", "function"]
       has_code = any(indicator in response_text for indicator in code_indicators)
       
       # Check minimum length
       min_length = kwargs.get("min_length", 50)
       is_long_enough = len(response_text) >= min_length
       
       return has_code and is_long_enough

   async def verified_coding_batch():
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.3,
           max_completion_tokens=500,
           system_instruction="You are a coding assistant. Always provide working code examples.",
           verification_callback=verify_code_response,
           verification_callback_args={"min_length": 100},
           max_retries=3
       )
       
       coding_prompts = [
           "Write a Python function to calculate fibonacci numbers",
           "Create a class for a simple calculator in Python",
           "Write a function to reverse a string in Python"
       ]
       
       results = await process_prompts_batch(
           config=config,
           provider="openai",
           prompts=coding_prompts,
           cache_dir="coding_cache"
       )
       
       for prompt_id, response in results.items():
           if "error" in response:
               print(f"Failed verification: {response['error']}")
           else:
               print(f"Verified code response for {prompt_id}")
               print(response['response_text'])
               print("-" * 80)

   asyncio.run(verified_coding_batch())

Multi-Provider Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def compare_providers():
       """Compare responses from different providers."""
       
       # Common prompts for comparison
       prompts = [
           "Explain quantum computing in simple terms",
           "What are the benefits of renewable energy?",
           "How does machine learning work?"
       ]
       
       # OpenAI configuration
       openai_config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=200
       )
       
       # Together.ai configuration
       together_config = LLMConfig(
           model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
           temperature=0.7,
           max_completion_tokens=200
       )
       
       # Process with both providers
       openai_results = await process_prompts_batch(
           config=openai_config,
           provider="openai",
           prompts=prompts,
           cache_dir="openai_comparison"
       )
       
       together_results = await process_prompts_batch(
           config=together_config,
           provider="together",
           prompts=prompts,
           cache_dir="together_comparison"
       )
       
       # Compare results
       for i, prompt in enumerate(prompts):
           prompt_id = list(openai_results.keys())[i]
           
           print(f"Prompt: {prompt}")
           print(f"OpenAI: {openai_results[prompt_id]['response_text']}")
           print(f"Together.ai: {together_results[prompt_id]['response_text']}")
           print("=" * 80)

   asyncio.run(compare_providers())

Large-Scale Processing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import json
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def large_scale_processing():
       """Process a large dataset efficiently."""
       
       # Load prompts from JSON file
       with open("large_dataset.json", "r") as f:
           data = json.load(f)
       
       prompts = [item["prompt"] for item in data]
       
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=150,
           max_concurrent_requests=10,  # Higher concurrency
           max_retries=5
       )
       
       # Process in batches to manage memory
       batch_size = 100
       all_results = {}
       
       for i in range(0, len(prompts), batch_size):
           batch_prompts = prompts[i:i + batch_size]
           
           print(f"Processing batch {i//batch_size + 1}/{(len(prompts)-1)//batch_size + 1}")
           
           batch_results = await process_prompts_batch(
               config=config,
               provider="openai",
               prompts=batch_prompts,
               cache_dir="large_scale_cache",
               desc=f"Batch {i//batch_size + 1}"
           )
           
           all_results.update(batch_results)
           
           # Optional: Save intermediate results
           with open(f"results_batch_{i//batch_size + 1}.json", "w") as f:
               json.dump(batch_results, f, indent=2)
       
       # Save final results
       with open("final_results.json", "w") as f:
           json.dump(all_results, f, indent=2)
       
       print(f"Processed {len(all_results)} prompts successfully")

   asyncio.run(large_scale_processing())

Content Generation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def content_generation_pipeline():
       """Generate content with multiple stages."""
       
       # Stage 1: Generate topics
       topic_config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.8,
           max_completion_tokens=50,
           system_instruction="Generate creative topic ideas."
       )
       
       topic_prompts = [
           "Suggest 3 interesting topics about artificial intelligence",
           "Suggest 3 interesting topics about space exploration",
           "Suggest 3 interesting topics about environmental science"
       ]
       
       topic_results = await process_prompts_batch(
           config=topic_config,
           provider="openai",
           prompts=topic_prompts,
           cache_dir="topics_cache"
       )
       
       # Stage 2: Generate detailed content for each topic
       content_config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=300,
           system_instruction="Write detailed, informative content about the given topic."
       )
       
       # Extract topics and create content prompts
       content_prompts = []
       for response in topic_results.values():
           topics_text = response['response_text']
           # Simple parsing - in practice, you might use more sophisticated parsing
           lines = [line.strip() for line in topics_text.split('\n') if line.strip()]
           for line in lines:
               if line:
                   content_prompts.append(f"Write a detailed explanation about: {line}")
       
       content_results = await process_prompts_batch(
           config=content_config,
           provider="openai",
           prompts=content_prompts,
           cache_dir="content_cache",
           desc="Generating detailed content"
       )
       
       # Stage 3: Generate summaries
       summary_config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.3,
           max_completion_tokens=100,
           system_instruction="Create concise summaries of the given content."
       )
       
       summary_prompts = [
           f"Summarize this content in 2-3 sentences: {response['response_text']}"
           for response in content_results.values()
       ]
       
       summary_results = await process_prompts_batch(
           config=summary_config,
           provider="openai",
           prompts=summary_prompts,
           cache_dir="summary_cache",
           desc="Generating summaries"
       )
       
       # Combine results
       final_content = []
       content_list = list(content_results.values())
       summary_list = list(summary_results.values())
       
       for i, (content, summary) in enumerate(zip(content_list, summary_list)):
           final_content.append({
               "id": i + 1,
               "full_content": content['response_text'],
               "summary": summary['response_text'],
               "word_count": len(content['response_text'].split())
           })
       
       return final_content

   # Run the pipeline
   content = asyncio.run(content_generation_pipeline())
   for item in content:
       print(f"Content {item['id']} ({item['word_count']} words):")
       print(f"Summary: {item['summary']}")
       print("-" * 50)

Error Handling Examples
-----------------------

Robust Error Handling
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from llm_batch_helper import LLMConfig, process_prompts_batch

   async def robust_processing():
       """Example with comprehensive error handling."""
       
       config = LLMConfig(
           model_name="gpt-4o-mini",
           temperature=0.7,
           max_completion_tokens=200,
           max_retries=3
       )
       
       prompts = [
           "Valid prompt 1",
           "",  # Empty prompt
           "Valid prompt 2",
           "A" * 10000,  # Very long prompt that might cause issues
           "Valid prompt 3"
       ]
       
       try:
           results = await process_prompts_batch(
               config=config,
               provider="openai",
               prompts=prompts,
               cache_dir="error_handling_cache"
           )
           
           # Process results and handle errors
           successful_responses = 0
           failed_responses = 0
           
           for prompt_id, response in results.items():
               if "error" in response:
                   print(f"Error in {prompt_id}: {response['error']}")
                   failed_responses += 1
               else:
                   print(f"Success {prompt_id}: {len(response['response_text'])} characters")
                   successful_responses += 1
           
           print(f"\nSummary: {successful_responses} successful, {failed_responses} failed")
           
       except Exception as e:
           print(f"Unexpected error: {e}")

   asyncio.run(robust_processing())