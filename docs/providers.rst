Provider Support
================

LLM Batch Helper supports multiple LLM providers. Each provider has specific configuration requirements and supported models.

Supported Providers
-------------------

OpenAI
~~~~~~

The OpenAI provider supports all OpenAI chat completion models.

**Setup:**

.. code-block:: bash

   export OPENAI_API_KEY="your-openai-api-key"

**Supported Models:**

- ``gpt-4o``
- ``gpt-4o-mini``
- ``gpt-4``
- ``gpt-4-turbo``
- ``gpt-3.5-turbo``

**Example:**

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   config = LLMConfig(
       model_name="gpt-4o-mini",
       temperature=0.7,
       max_completion_tokens=500
   )

   results = await process_prompts_batch(
       config=config,
       provider="openai",
       prompts=your_prompts
   )

Together.ai
~~~~~~~~~~~

The Together.ai provider supports various open-source models hosted on Together.ai.

**Setup:**

.. code-block:: bash

   export TOGETHER_API_KEY="your-together-api-key"

**Popular Models:**

- ``meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo``
- ``meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo``
- ``mistralai/Mixtral-8x7B-Instruct-v0.1``
- ``NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO``
- ``togethercomputer/RedPajama-INCITE-Chat-3B-v1``

**Example:**

.. code-block:: python

   from llm_batch_helper import LLMConfig, process_prompts_batch

   config = LLMConfig(
       model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
       temperature=0.8,
       max_completion_tokens=300,
       system_instruction="You are a helpful AI assistant."
   )

   results = await process_prompts_batch(
       config=config,
       provider="together",
       prompts=your_prompts
   )

Provider Comparison
-------------------

.. list-table::
   :header-rows: 1

   * - Feature
     - OpenAI
     - Together.ai
   * - Model Variety
     - OpenAI models only
     - Many open-source models
   * - Pricing
     - Per-token pricing
     - Competitive pricing
   * - Rate Limits
     - Tier-based limits
     - Model-dependent limits
   * - Response Quality
     - Very high (GPT-4)
     - Varies by model
   * - Speed
     - Fast
     - Varies by model

Configuration Best Practices
-----------------------------

Temperature Settings
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # For factual/deterministic responses
   config = LLMConfig(temperature=0.0)
   
   # For balanced creativity
   config = LLMConfig(temperature=0.7)
   
   # For highly creative responses
   config = LLMConfig(temperature=1.0)

Concurrency Management
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Conservative (good for testing)
   config = LLMConfig(max_concurrent_requests=2)
   
   # Balanced (recommended)
   config = LLMConfig(max_concurrent_requests=5)
   
   # Aggressive (for high-throughput)
   config = LLMConfig(max_concurrent_requests=10)

Token Management
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Short responses
   config = LLMConfig(max_completion_tokens=100)
   
   # Medium responses  
   config = LLMConfig(max_completion_tokens=500)
   
   # Long responses
   config = LLMConfig(max_completion_tokens=2000)

Error Handling by Provider
---------------------------

Each provider may have different error conditions:

**OpenAI Errors:**

- Rate limit exceeded
- Invalid API key
- Model not found
- Token limit exceeded

**Together.ai Errors:**

- Rate limit exceeded
- Invalid API key
- Model not available
- Request timeout

The package automatically retries on transient errors with exponential backoff.

Advanced Usage
--------------

Custom System Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   config = LLMConfig(
       model_name="gpt-4o-mini",
       system_instruction="""
       You are an expert technical writer. 
       Always provide clear, concise explanations.
       Include code examples when relevant.
       """
   )

Provider-Specific Optimizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # OpenAI: Optimized for speed
   openai_config = LLMConfig(
       model_name="gpt-4o-mini",
       max_concurrent_requests=10,
       temperature=0.7
   )

   # Together.ai: Optimized for cost
   together_config = LLMConfig(
       model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
       max_concurrent_requests=5,
       temperature=0.8
   )