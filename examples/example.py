import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the package
sys.path.append(str(Path(__file__).parent.parent))
from llm_batch_helper import LLMConfig, process_prompts_batch


def example_verification_callback(
    prompt_id: str, llm_response_data: dict, original_prompt_text: str, **kwargs
) -> bool:
    """Example verification callback that checks if the response is not empty."""
    if not llm_response_data.get("response_text"):
        print(f"Verification failed for {prompt_id}: Empty response")
        return False
    return True


def run_batch(config, cache_dir, force, run_label, **kwargs):
    print(f"\n=== {run_label} (force={force}, cache_dir='{cache_dir}') ===")
    results = process_prompts_batch(
        config=config,
        provider="openai",
        desc=f"{run_label}",
        cache_dir=cache_dir,
        force=force,
        **kwargs,
    )
    for prompt_id, response in results.items():
        if response.get("from_cache"):
            status = "[CACHE]"
        elif "error" in response:
            status = "[ERROR]"
        else:
            status = "[GENERATED]"
        if "error" in response:
            print(f"{status} Error for {prompt_id}: {response['error']}")
        elif "response_text" in response:
            print(f"{status} Success for {prompt_id}: {response['response_text']}")
        else:
            print(f"{status} Unhandled response for {prompt_id}: {response}")


def main():
    cache_dir = "llm_cache"
    # Create a configuration for OpenAI
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=1.0,
        max_completion_tokens=100,
        max_retries=3,
        max_concurrent_requests=2,
        verification_callback=example_verification_callback,
        verification_callback_args={"min_length": 10},
    )

    # Example 1: List-based prompts
    print("\n=== Example 1: List-based Prompts ===")
    list_prompts = [
        "What is the capital of France? Answer concisely.",  # String format
        "What is 2+2? Answer concisely.",  # String format
        "Who wrote 'Hamlet'? Answer concisely.",  # String format
    ]

    # Run the list-based prompts
    run_batch(
        config=config,
        cache_dir=cache_dir,
        force=False,
        run_label="List-based Prompts",
        prompts=list_prompts,
    )

    # Example 2: Folder-based prompts
    print("\n=== Example 2: Folder-based Prompts ===")
    # Create example prompts directory and files
    prompts_dir = "example_prompts"
    os.makedirs(prompts_dir, exist_ok=True)

    example_prompts = {
        "france": "What is the capital of France? Answer concisely.",
        "math": "What is 2+2? Answer concisely.",
        "shakespeare": "Who wrote 'Hamlet'? Answer concisely.",
    }

    for filename, content in example_prompts.items():
        with open(os.path.join(prompts_dir, f"{filename}.txt"), "w") as f:
            f.write(content)

    # Run the folder-based prompts
    run_batch(
        config=config,
        cache_dir=cache_dir,
        force=False,
        run_label="Folder-based Prompts",
        input_dir=prompts_dir,
    )


if __name__ == "__main__":
    main()
