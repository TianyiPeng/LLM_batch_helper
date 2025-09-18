import asyncio
import os
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import warnings

import httpx
import openai
import google.generativeai as genai
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential, before_sleep_log
from tqdm.asyncio import tqdm_asyncio

from .cache import LLMCache
from .config import LLMConfig
from .input_handlers import get_prompts


def _run_async_function(async_func, *args, **kwargs):
    """
    Run an async function in a way that works in both regular Python and Jupyter notebooks.
    
    This handles the event loop management properly for different environments.
    """
    try:
        # Try to get the current event loop
        loop = asyncio.get_running_loop()
        # If we're in a running loop (like Jupyter), we need to use nest_asyncio
        try:
            import nest_asyncio
            nest_asyncio.apply()
            return asyncio.run(async_func(*args, **kwargs))
        except ImportError:
            # If nest_asyncio is not available, try to run in the current loop
            # This is a fallback that might work in some cases
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                return future.result()
    except RuntimeError:
        # No event loop running, we can use asyncio.run directly
        return asyncio.run(async_func(*args, **kwargs))


def log_retry_attempt(retry_state):
    """Custom logging function for retry attempts."""
    attempt_number = retry_state.attempt_number
    exception = retry_state.outcome.exception()
    wait_time = retry_state.next_action.sleep if retry_state.next_action else 0
    
    error_type = type(exception).__name__
    error_msg = str(exception)
    
    # Extract status code if available
    status_code = "unknown"
    if hasattr(exception, 'status_code'):
        status_code = exception.status_code
    elif hasattr(exception, 'response') and hasattr(exception.response, 'status_code'):
        status_code = exception.response.status_code
    
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Retry attempt {attempt_number}/5:")
    print(f"   Error: {error_type} (status: {status_code})")
    print(f"   Message: {error_msg[:100]}{'...' if len(error_msg) > 100 else ''}")
    print(f"   Waiting {wait_time:.1f}s before next attempt...")
    print()


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(
        (
            ConnectionError,
            TimeoutError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.RateLimitError,
            openai.APIError,
        )
    ),
    before_sleep=log_retry_attempt,
    reraise=True,
)
async def _get_openai_response_direct(
    prompt: str, config: LLMConfig
) -> Dict[str, Union[str, Dict]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    async with httpx.AsyncClient(timeout=1000.0) as client:
        aclient = openai.AsyncOpenAI(api_key=api_key, http_client=client)
        messages = [
            {"role": "system", "content": config.system_instruction},
            {"role": "user", "content": prompt},
        ]

        response = await aclient.chat.completions.create(
            model=config.model_name,
            messages=messages,
            temperature=config.temperature,
            max_completion_tokens=config.max_completion_tokens,
            **config.kwargs,
        )
        usage_details = {
            "prompt_token_count": response.usage.prompt_tokens,
            "completion_token_count": response.usage.completion_tokens,
            "total_token_count": response.usage.total_tokens,
        }
        return {
            "response_text": response.choices[0].message.content,
            "usage_details": usage_details,
        }


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(
        (
            ConnectionError,
            TimeoutError,
            httpx.HTTPStatusError,
            httpx.RequestError,
        )
    ),
    reraise=True,
)
async def _get_together_response_direct(
    prompt: str, config: LLMConfig
) -> Dict[str, Union[str, Dict]]:
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable not set")

    async with httpx.AsyncClient(timeout=1000.0) as client:
        messages = [
            {"role": "system", "content": config.system_instruction},
            {"role": "user", "content": prompt},
        ]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": config.model_name,
            "messages": messages,
            "temperature": config.temperature,
            "max_tokens": config.max_completion_tokens,
            **config.kwargs,
        }

        response = await client.post(
            "https://api.together.xyz/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        
        response_data = response.json()
        usage = response_data.get("usage", {})
        usage_details = {
            "prompt_token_count": usage.get("prompt_tokens", 0),
            "completion_token_count": usage.get("completion_tokens", 0),
            "total_token_count": usage.get("total_tokens", 0),
        }
        
        return {
            "response_text": response_data["choices"][0]["message"]["content"],
            "usage_details": usage_details,
        }


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(
        (
            ConnectionError,
            TimeoutError,
            httpx.HTTPStatusError,
            httpx.RequestError,
        )
    ),
    before_sleep=log_retry_attempt,
    reraise=True,
)
async def _get_openrouter_response_direct(
    prompt: str, config: LLMConfig
) -> Dict[str, Union[str, Dict]]:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")

    async with httpx.AsyncClient(timeout=1000.0) as client:
        messages = [
            {"role": "system", "content": config.system_instruction},
            {"role": "user", "content": prompt},
        ]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": config.model_name,
            "messages": messages,
            "temperature": config.temperature,
            "max_tokens": config.max_completion_tokens,
            **config.kwargs,
        }

        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        
        response_data = response.json()
        usage = response_data.get("usage", {})
        usage_details = {
            "prompt_token_count": usage.get("prompt_tokens", 0),
            "completion_token_count": usage.get("completion_tokens", 0),
            "total_token_count": usage.get("total_tokens", 0),
        }
        
        return {
            "response_text": response_data["choices"][0]["message"]["content"],
            "usage_details": usage_details,
        }


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(
        (
            ConnectionError,
            TimeoutError,
            Exception,  # Gemini SDK may raise various exceptions
        )
    ),
    before_sleep=log_retry_attempt,
    reraise=True,
)
async def _get_gemini_response_direct(
    prompt: str, config: LLMConfig
) -> Dict[str, Union[str, Dict]]:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")

    # Configure the Gemini client
    genai.configure(api_key=api_key)
    
    # Create the model
    model = genai.GenerativeModel(config.model_name)
    
    # Prepare the prompt with system instruction if provided
    full_prompt = prompt
    if config.system_instruction and config.system_instruction.strip():
        full_prompt = f"{config.system_instruction}\n\n{prompt}"
    
    try:
        # Generate content asynchronously
        response = await asyncio.to_thread(
            model.generate_content,
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=config.temperature,
                max_output_tokens=config.max_completion_tokens,
                **{k: v for k, v in config.kwargs.items() if k in ['top_p', 'top_k', 'candidate_count']}
            )
        )
        
        # Extract usage information if available
        usage_details = {
            "prompt_token_count": getattr(response.usage_metadata, 'prompt_token_count', 0) if hasattr(response, 'usage_metadata') else 0,
            "completion_token_count": getattr(response.usage_metadata, 'candidates_token_count', 0) if hasattr(response, 'usage_metadata') else 0,
            "total_token_count": getattr(response.usage_metadata, 'total_token_count', 0) if hasattr(response, 'usage_metadata') else 0,
        }
        
        return {
            "response_text": response.text,
            "usage_details": usage_details,
        }
        
    except Exception as e:
        # Handle potential safety blocks or other Gemini-specific errors
        if hasattr(e, 'message') and 'block' in str(e).lower():
            return {
                "response_text": "[Content blocked by safety filters]",
                "usage_details": {"prompt_token_count": 0, "completion_token_count": 0, "total_token_count": 0},
                "blocked": True
            }
        raise e


async def get_llm_response_with_internal_retry(
    prompt_id: str,
    prompt: str,
    config: LLMConfig,
    provider: str,
    cache: Optional[LLMCache] = None,
    force: bool = False,
) -> Dict[str, Union[str, Dict]]:
    # Check cache first if available and not forcing regeneration
    if cache and not force:
        cached_response = cache.get_cached_response(prompt_id)
        if cached_response:
            return cached_response["llm_response"]

    try:
        if provider.lower() == "openai":
            response = await _get_openai_response_direct(prompt, config)
        elif provider.lower() == "together":
            response = await _get_together_response_direct(prompt, config)
        elif provider.lower() == "openrouter":
            response = await _get_openrouter_response_direct(prompt, config)
        elif provider.lower() == "gemini":
            response = await _get_gemini_response_direct(prompt, config)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Cache the response if cache is available
        if cache and "error" not in response:
            cache.save_response(prompt_id, prompt, response)

        return response
    except Exception as e:
        return {
            "error": f"LLM API call failed after internal retries: {e!s}",
            "provider": provider,
        }


async def process_prompts_batch_async(
    prompts: Optional[List[Union[str, Tuple[str, str], Dict[str, Any]]]] = None,
    input_dir: Optional[str] = None,
    config: LLMConfig = None,
    provider: str = "openai",
    desc: str = "Processing prompts",
    cache_dir: Optional[str] = None,
    force: bool = False,
) -> Dict[str, Dict[str, Union[str, Dict]]]:
    """Process a batch of prompts through the LLM.

    Args:
        prompts: Optional list of prompts in any supported format (string, tuple, or dict)
        input_dir: Optional path to directory containing prompt files
        config: LLM configuration
        provider: LLM provider to use ("openai", "together", "openrouter", or "gemini")
        desc: Description for progress bar
        cache_dir: Optional directory for caching responses
        force: If True, force regeneration even if cached response exists

    Returns:
        Dict mapping prompt IDs to their responses, ordered by input sequence

    Note:
        Either prompts or input_dir must be provided, but not both.
        Results are returned in the same order as the input prompts.
    """
    if prompts is None and input_dir is None:
        raise ValueError("Either prompts or input_dir must be provided")
    if prompts is not None and input_dir is not None:
        raise ValueError("Cannot specify both prompts and input_dir")

    # Get prompts from either source
    if input_dir is not None:
        prompts = get_prompts(input_dir)
    else:
        prompts = get_prompts(prompts)

    # Create semaphore for concurrent requests
    semaphore = asyncio.Semaphore(config.max_concurrent_requests)

    # Process prompts
    results = {}
    # Keep track of original order for sorting results
    prompt_order = {prompt_id: idx for idx, (prompt_id, _) in enumerate(prompts)}
    
    tasks = [
        _process_single_prompt_attempt_with_verification(
            prompt_id, prompt_text, config, provider, semaphore, cache_dir, force
        )
        for prompt_id, prompt_text in prompts
    ]

    for future in tqdm_asyncio(asyncio.as_completed(tasks), total=len(tasks), desc=desc):
        prompt_id, response_data = await future
        results[prompt_id] = response_data

    # Sort results by original input order to maintain input sequence
    # Note: Python 3.7+ guarantees dict insertion order, we explicitly sort
    # to ensure results match the original prompt order regardless of completion order
    ordered_results = {}
    for prompt_id in sorted(results.keys(), key=lambda pid: prompt_order[pid]):
        ordered_results[prompt_id] = results[prompt_id]
    
    return ordered_results


def process_prompts_batch(
    prompts: Optional[List[Union[str, Tuple[str, str], Dict[str, Any]]]] = None,
    input_dir: Optional[str] = None,
    config: LLMConfig = None,
    provider: str = "openai",
    desc: str = "Processing prompts",
    cache_dir: Optional[str] = None,
    force: bool = False,
) -> Dict[str, Dict[str, Union[str, Dict]]]:
    """
    Process a batch of prompts through the LLM (synchronous version).
    
    This is the main user-facing function that works in both regular Python scripts
    and Jupyter notebooks without requiring async/await syntax.
    
    Args:
        prompts: Optional list of prompts in any supported format (string, tuple, or dict)
        input_dir: Optional path to directory containing prompt files
        config: LLM configuration
        provider: LLM provider to use ("openai", "together", "openrouter", or "gemini")
        desc: Description for progress bar
        cache_dir: Optional directory for caching responses
        force: If True, force regeneration even if cached response exists

    Returns:
        Dict mapping prompt IDs to their responses, ordered by input sequence

    Note:
        Either prompts or input_dir must be provided, but not both.
        Results are returned in the same order as the input prompts.
        
    Example:
        >>> from llm_batch_helper import LLMConfig, process_prompts_batch
        >>> config = LLMConfig(model_name="gpt-4o-mini")
        >>> results = process_prompts_batch(
        ...     prompts=["What is 2+2?", "What is the capital of France?"],
        ...     config=config,
        ...     provider="openai"
        ... )
        >>> # Results will be in the same order as input prompts
    """
    return _run_async_function(
        process_prompts_batch_async,
        prompts=prompts,
        input_dir=input_dir,
        config=config,
        provider=provider,
        desc=desc,
        cache_dir=cache_dir,
        force=force,
    )


async def _process_single_prompt_attempt_with_verification(
    prompt_id: str,
    prompt_text: str,
    config: LLMConfig,
    provider: str,
    semaphore: asyncio.Semaphore,
    cache_dir: Optional[str] = None,
    force: bool = False,
):
    """Process a single prompt with verification and caching."""
    async with semaphore:
        # Check cache first if cache_dir is provided
        if cache_dir and not force:
            cache = LLMCache(cache_dir)
            cached_response = cache.get_cached_response(prompt_id)
            if cached_response is not None:
                cached_response_data = cached_response["llm_response"]
                
                # If no verification callback, use cached response directly
                if config.verification_callback is None:
                    return prompt_id, {**cached_response_data, "from_cache": True}
                
                # Verify response if callback provided
                verified = await asyncio.to_thread(
                    config.verification_callback,
                    prompt_id,
                    cached_response_data,
                    prompt_text,
                    **config.verification_callback_args,
                )
                if verified:
                    return prompt_id, {**cached_response_data, "from_cache": True}

        # Process the prompt
        last_exception_details = None
        for attempt in range(config.max_retries):
            if attempt > 0:
                print(f"🔁 [{datetime.now().strftime('%H:%M:%S')}] Application-level retry {attempt+1}/{config.max_retries} for prompt: {prompt_id}")
            
            try:
                # Get LLM response
                llm_response_data = await get_llm_response_with_internal_retry(
                    prompt_id, prompt_text, config, provider
                )

                if "error" in llm_response_data:
                    print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] API call failed on attempt {attempt+1}: {llm_response_data.get('error', 'Unknown error')}")
                    last_exception_details = llm_response_data
                    if attempt < config.max_retries - 1:
                        wait_time = min(2 * 2**attempt, 30)
                        print(f"   Waiting {wait_time}s before next application retry...")
                        await asyncio.sleep(wait_time)
                    continue

                # Verify response if callback provided
                if config.verification_callback:
                    verified = await asyncio.to_thread(
                        config.verification_callback,
                        prompt_id,
                        llm_response_data,
                        prompt_text,
                        **config.verification_callback_args,
                    )
                    if not verified:
                        last_exception_details = {
                            "error": f"Verification failed on attempt {attempt + 1}",
                            "prompt_id": prompt_id,
                            "llm_response_data": llm_response_data,
                        }
                        if attempt == config.max_retries - 1:
                            return prompt_id, last_exception_details
                        continue

                # Save to cache if cache_dir provided
                if cache_dir:
                    cache = LLMCache(cache_dir)
                    cache.save_response(prompt_id, prompt_text, llm_response_data)

                return prompt_id, llm_response_data

            except Exception as e:
                last_exception_details = {
                    "error": f"Unexpected error: {e!s}",
                    "prompt_id": prompt_id,
                }
                if attempt == config.max_retries - 1:
                    return prompt_id, last_exception_details
                # Sleep is now handled above with logging
                continue

        return prompt_id, last_exception_details or {
            "error": f"Exhausted all {config.max_retries} retries for {prompt_id}"
        }
