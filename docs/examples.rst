Examples
========

This page contains practical examples demonstrating various features of LLM Batch Helper.

**🎉 New in v0.3.0**: All examples use the simplified API - no async/await syntax needed!

Basic Examples
--------------

Simple Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   # Create configuration
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.7,
       max_completion_tokens=100
   )
   
   # Define prompts
   prompts = [
       "What is machine learning?",
       "Explain neural networks briefly.",
       "What is deep learning?"
   ]
   
   # Process prompts - no async/await needed!
   results = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=prompts,
       cache_dir="ml_cache"
   )
   
   # Display results
   for prompt_id, response in results.items():
       status = "[CACHE]" if response.get("from_cache") else "[GENERATED]"
       print(f"{status} Q: What is machine learning related topic?")
       print(f"A: {response['response_text']}\n")

File-Based Processing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from llm_batch_helper import LLMConfig, process_prompts_batch

   # Create configuration
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.5,
       max_completion_tokens=300,
       system_instruction="You are a helpful assistant providing detailed explanations."
   )
   
   # Process all .txt files in the 'questions' directory
   results = process_prompts_batch(
       config=config,
       provider="openai",
       input_dir="questions",  # Directory containing .txt files
       cache_dir="answers_cache",
       desc="Processing question files"
   )
   
   # Create answers directory if it doesn't exist
   os.makedirs("answers", exist_ok=True)
   
   # Save results to files
   for prompt_id, response in results.items():
       status = "[CACHE]" if response.get("from_cache") else "[GENERATED]"
       if "error" not in response:
           with open(f"answers/{prompt_id}_answer.txt", "w") as f:
               f.write(response['response_text'])
           print(f"{status} Saved answer for {prompt_id}")
       else:
           print(f"❌ Error for {prompt_id}: {response['error']}")

Advanced Examples
-----------------

Custom Verification
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

   # Create configuration with custom verification
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.3,
       max_completion_tokens=500,
       system_instruction="You are a coding assistant. Always provide working code examples.",
       verification_callback=verify_code_response,
       verification_callback_args={"min_length": 100},
       max_retries=3
   )
   
   # Define coding prompts
   coding_prompts = [
       "Write a Python function to calculate fibonacci numbers",
       "Create a class for a simple calculator in Python", 
       "Write a function to reverse a string in Python"
   ]
   
   # Process with verification - no async/await needed!
   results = process_prompts_batch(
       config=config,
       provider="openai",
       prompts=coding_prompts,
       cache_dir="coding_cache"
   )
   
   # Display results
   for prompt_id, response in results.items():
       status = "[CACHE]" if response.get("from_cache") else "[GENERATED]"
       if "error" in response:
           print(f"❌ Failed verification for {prompt_id}: {response['error']}")
       else:
           print(f"✅ {status} Verified code response for {prompt_id}")
           print(response['response_text'])
           print("-" * 80)

Multi-Provider Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

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
   
   # OpenRouter configuration (recommended for variety)
   openrouter_config = LLMConfig(
       model_name="anthropic/claude-3-5-sonnet",
       temperature=0.7,
       max_completion_tokens=200
   )
   
   print("🚀 Processing prompts with multiple providers...")
   
   # Process with OpenAI
   print("Processing with OpenAI...")
   openai_results = process_prompts_batch(
       config=openai_config,
       provider="openai",
       prompts=prompts,
       cache_dir="openai_comparison"
   )
   
   # Process with OpenRouter
   print("Processing with OpenRouter...")
   openrouter_results = process_prompts_batch(
       config=openrouter_config,
       provider="openrouter", 
       prompts=prompts,
       cache_dir="openrouter_comparison"
   )
   
   # Compare results
   print("\n📊 Comparison Results:")
   print("=" * 80)
   
   for i, prompt in enumerate(prompts):
       openai_ids = list(openai_results.keys())
       openrouter_ids = list(openrouter_results.keys())
       
       if i < len(openai_ids) and i < len(openrouter_ids):
           openai_response = openai_results[openai_ids[i]]
           openrouter_response = openrouter_results[openrouter_ids[i]]
           
           print(f"\n🔍 Prompt: {prompt}")
           print(f"🤖 OpenAI: {openai_response['response_text'][:100]}...")
           print(f"🧠 OpenRouter: {openrouter_response['response_text'][:100]}...")
           print("-" * 80)

Large-Scale Processing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   from llm_batch_helper import LLMConfig, process_prompts_batch

   # Load prompts from JSON file (example format)
   # large_dataset.json should contain: [{"prompt": "text1"}, {"prompt": "text2"}, ...]
   try:
       with open("large_dataset.json", "r") as f:
           data = json.load(f)
       prompts = [item["prompt"] for item in data]
   except FileNotFoundError:
       # Create example dataset if file doesn't exist
       prompts = [
           f"Generate a creative story about topic {i}" for i in range(1, 51)
       ]
       print("📝 Using example dataset (50 prompts)")
   
   # Configuration for large-scale processing
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.7,
       max_completion_tokens=150,
       max_concurrent_requests=10,  # Higher concurrency for speed
       max_retries=5
   )
   
   print(f"🚀 Processing {len(prompts)} prompts in batches...")
   
   # Process in batches to manage memory and API limits
   batch_size = 20  # Smaller batches for better control
   all_results = {}
   
   for i in range(0, len(prompts), batch_size):
       batch_prompts = prompts[i:i + batch_size]
       batch_num = i//batch_size + 1
       total_batches = (len(prompts)-1)//batch_size + 1
       
       print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch_prompts)} prompts)")
       
       # Process current batch - no async/await needed!
       batch_results = process_prompts_batch(
           config=config,
           provider="openai",
           prompts=batch_prompts,
           cache_dir="large_scale_cache",
           desc=f"Batch {batch_num}"
       )
       
       all_results.update(batch_results)
       
       # Save intermediate results
       with open(f"results_batch_{batch_num}.json", "w") as f:
           json.dump(batch_results, f, indent=2)
       
       print(f"✅ Batch {batch_num} completed: {len(batch_results)} responses")
   
   # Save final consolidated results
   with open("final_results.json", "w") as f:
       json.dump(all_results, f, indent=2)
   
   # Summary
   successful = sum(1 for r in all_results.values() if "error" not in r)
   failed = len(all_results) - successful
   
   print(f"\n📊 Processing Complete!")
   print(f"✅ Successful: {successful}")
   print(f"❌ Failed: {failed}")
   print(f"📁 Results saved to: final_results.json")

Content Generation Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   print("🏗️  Starting Content Generation Pipeline...")
   
   # Stage 1: Generate topics
   print("\n📝 Stage 1: Generating topics...")
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
   
   # Generate topics - no async/await needed!
   topic_results = process_prompts_batch(
       config=topic_config,
       provider="openai",
       prompts=topic_prompts,
       cache_dir="topics_cache"
   )
   
   # Stage 2: Generate detailed content for each topic
   print("\n📖 Stage 2: Generating detailed content...")
   content_config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.7,
       max_completion_tokens=300,
       system_instruction="Write detailed, informative content about the given topic."
   )
   
   # Extract topics and create content prompts
   content_prompts = []
   for prompt_id, response in topic_results.items():
       if "error" not in response:
           topics_text = response['response_text']
           # Simple parsing - extract lines that look like topics
           lines = [line.strip() for line in topics_text.split('\n') if line.strip()]
           for line in lines[:3]:  # Take first 3 topics per category
               if line and not line.startswith("#"):
                   content_prompts.append(f"Write a detailed explanation about: {line}")
   
   # Generate detailed content
   content_results = process_prompts_batch(
       config=content_config,
       provider="openai",
       prompts=content_prompts,
       cache_dir="content_cache",
       desc="Generating detailed content"
   )
   
   # Stage 3: Generate summaries
   print("\n📋 Stage 3: Generating summaries...")
   summary_config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.3,
       max_completion_tokens=100,
       system_instruction="Create concise summaries of the given content."
   )
   
   # Create summary prompts from successful content
   summary_prompts = []
   content_items = []
   for response in content_results.values():
       if "error" not in response and len(response['response_text']) > 50:
           summary_prompts.append(f"Summarize this content in 2-3 sentences: {response['response_text']}")
           content_items.append(response)
   
   # Generate summaries
   summary_results = process_prompts_batch(
       config=summary_config,
       provider="openai",
       prompts=summary_prompts,
       cache_dir="summary_cache",
       desc="Generating summaries"
   )
   
   # Combine and display results
   print("\n🎯 Pipeline Results:")
   print("=" * 60)
   
   summary_list = list(summary_results.values())
   for i, (content, summary) in enumerate(zip(content_items, summary_list)):
       if "error" not in summary:
           word_count = len(content['response_text'].split())
           print(f"\n📄 Content {i + 1} ({word_count} words):")
           print(f"📝 Summary: {summary['response_text']}")
           print(f"💾 Full content available in results")
           print("-" * 40)
   
   print(f"\n✅ Pipeline completed! Generated {len(content_items)} pieces of content.")

Error Handling Examples
-----------------------

Robust Error Handling
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   print("🛡️  Testing Robust Error Handling...")
   
   # Create configuration with retry settings
   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.7,
       max_completion_tokens=200,
       max_retries=3  # Will retry failed requests
   )
   
   # Test prompts including some that might cause issues
   test_prompts = [
       "What is the capital of France?",  # Valid prompt
       "",  # Empty prompt - might cause issues
       "Explain quantum physics briefly.",  # Valid prompt
       "A" * 8000,  # Very long prompt - might hit token limits
       "What is 2+2?",  # Valid prompt
       {"id": "custom_test", "text": "Dictionary format test"}  # Mixed format
   ]
   
   print(f"📝 Processing {len(test_prompts)} test prompts...")
   
   try:
       # Process with error handling - no async/await needed!
       results = process_prompts_batch(
           config=config,
           provider="openai",
           prompts=test_prompts,
           cache_dir="error_handling_cache",
           desc="Error Handling Test"
       )
       
       # Analyze results and handle errors
       print("\n📊 Results Analysis:")
       print("=" * 50)
       
       successful_responses = 0
       failed_responses = 0
       cached_responses = 0
       
       for prompt_id, response in results.items():
           # Check response status
           if "error" in response:
               print(f"❌ Error in {prompt_id}: {response['error'][:100]}...")
               failed_responses += 1
           else:
               status_icon = "💾" if response.get("from_cache") else "✅"
               char_count = len(response['response_text'])
               print(f"{status_icon} Success {prompt_id}: {char_count} characters")
               successful_responses += 1
               if response.get("from_cache"):
                   cached_responses += 1
       
       # Summary statistics
       print(f"\n📈 Summary:")
       print(f"✅ Successful: {successful_responses}")
       print(f"❌ Failed: {failed_responses}")
       print(f"💾 From cache: {cached_responses}")
       print(f"📊 Success rate: {successful_responses/(successful_responses+failed_responses)*100:.1f}%")
       
   except Exception as e:
       print(f"💥 Unexpected error during processing: {e}")
       print("This might indicate a configuration or API key issue.")
   
   print("\n🎯 Error handling test completed!")