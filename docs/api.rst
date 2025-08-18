API Reference
=============

This page contains the complete API documentation for LLM Batch Helper.

Core Functions
--------------

.. autofunction:: llm_batch_helper.process_prompts_batch

Configuration
-------------

.. autoclass:: llm_batch_helper.LLMConfig
   :members:
   :undoc-members:
   :show-inheritance:

Caching
-------

.. autoclass:: llm_batch_helper.LLMCache
   :members:
   :undoc-members:
   :show-inheritance:

Input Handlers
--------------

.. autofunction:: llm_batch_helper.get_prompts

.. autofunction:: llm_batch_helper.read_prompt_files

.. autofunction:: llm_batch_helper.read_prompt_list

Provider Functions
------------------

Internal provider functions (for advanced users):

.. automodule:: llm_batch_helper.providers
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

.. automodule:: llm_batch_helper.exceptions
   :members:
   :undoc-members:
   :show-inheritance: