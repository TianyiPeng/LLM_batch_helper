import asyncio
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx
import openai
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from tqdm.asyncio import tqdm_asyncio

from .cache import LLMCache
from .config import LLMConfig
from .input_handlers import get_prompts


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


async def process_prompts_batch(
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
        provider: LLM provider to use ("openai", "together", or "gemini")
        desc: Description for progress bar
        cache_dir: Optional directory for caching responses
        force: If True, force regeneration even if cached response exists

    Returns:
        Dict mapping prompt IDs to their responses

    Note:
        Either prompts or input_dir must be provided, but not both.
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
    tasks = [
        _process_single_prompt_attempt_with_verification(
            prompt_id, prompt_text, config, provider, semaphore, cache_dir, force
        )
        for prompt_id, prompt_text in prompts
    ]

    for future in tqdm_asyncio(asyncio.as_completed(tasks), total=len(tasks), desc=desc):
        prompt_id, response_data = await future
        results[prompt_id] = response_data

    return results


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
                # Verify response if callback provided
                cached_response_data = cached_response["llm_response"]
                if config.verification_callback:
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
            try:
                # Get LLM response
                llm_response_data = await get_llm_response_with_internal_retry(
                    prompt_id, prompt_text, config, provider
                )

                if "error" in llm_response_data:
                    last_exception_details = llm_response_data
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
                        await asyncio.sleep(min(2 * 2**attempt, 30))
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
                await asyncio.sleep(min(2 * 2**attempt, 30))
                continue

        return prompt_id, last_exception_details or {
            "error": f"Exhausted all {config.max_retries} retries for {prompt_id}"
        }
