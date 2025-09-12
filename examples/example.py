"""
LLM Batch Helper Example Script

This example demonstrates the key features of LLM Batch Helper:
- Multiple input formats (string, tuple, dictionary)
- File-based processing
- Custom verification callbacks
- Caching functionality
- Error handling

🎉 New in v0.3.0: Simplified API - no async/await needed!
"""

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
    response_text = llm_response_data.get("response_text", "")
    min_length = kwargs.get("min_length", 10)
    
    if not response_text.strip():
        print(f"❌ Verification failed for {prompt_id}: Empty response")
        return False
    
    if len(response_text) < min_length:
        print(f"❌ Verification failed for {prompt_id}: Too short ({len(response_text)} < {min_length})")
        return False
    
    print(f"✅ Verification passed for {prompt_id}")
    return True


def run_batch(config, cache_dir, force, run_label, **kwargs):
    """Helper function to run a batch and display results."""
    print(f"\n{'='*60}")
    print(f"🚀 {run_label}")
    print(f"   Cache: {cache_dir} | Force: {force}")
    print(f"{'='*60}")
    
    # Process prompts - no async/await needed!
    results = process_prompts_batch(
        config=config,
        provider="openai",
        desc=f"{run_label}",
        cache_dir=cache_dir,
        force=force,
        **kwargs,
    )
    
    # Display results with enhanced formatting
    successful = 0
    cached = 0
    failed = 0
    
    for prompt_id, response in results.items():
        if "error" in response:
            status = "❌ [ERROR]"
            print(f"{status} {prompt_id}: {response['error'][:100]}...")
            failed += 1
        elif response.get("from_cache"):
            status = "💾 [CACHE]"
            print(f"{status} {prompt_id}: {response['response_text'][:100]}...")
            cached += 1
            successful += 1
        else:
            status = "✅ [GENERATED]"
            print(f"{status} {prompt_id}: {response['response_text'][:100]}...")
            successful += 1
    
    print(f"\n📊 Summary: {successful} successful ({cached} cached), {failed} failed")


def main():
    """Main example function demonstrating various features."""
    print("🎉 LLM Batch Helper Example Script")
    print("Using simplified v0.3.0+ API - no async/await needed!")
    
    cache_dir = "llm_cache"
    
    # Example 1: Multiple Input Formats
    print(f"\n{'🔧 CONFIGURATION':<60}")
    config_with_verification = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=100,
        max_retries=3,
        max_concurrent_requests=5,
        verification_callback=example_verification_callback,
        verification_callback_args={"min_length": 15},
    )
    
    print(f"✅ Created config with verification callback")
    print(f"   Model: {config_with_verification.model_name}")
    print(f"   Temperature: {config_with_verification.temperature}")
    print(f"   Max concurrent: {config_with_verification.max_concurrent_requests}")
    
    # Example 1: Multiple Input Formats
    print(f"\n{'📝 EXAMPLE 1: Multiple Input Formats':<60}")
    mixed_prompts = [
        # String format - ID will be auto-generated
        "What is the capital of France? Answer concisely.",
        
        # Tuple format - custom ID
        ("custom_math", "What is 2+2? Answer concisely."),
        
        # Dictionary format - both keys required
        {"id": "shakespeare_q", "text": "Who wrote 'Hamlet'? Answer concisely."},
        {"id": "science_q", "text": "What is photosynthesis? Answer briefly."},
    ]
    
    run_batch(
        config=config_with_verification,
        cache_dir=cache_dir,
        force=False,
        run_label="Mixed Input Formats",
        prompts=mixed_prompts,
    )

    # Example 2: Without Verification Callback (tests caching fix)
    print(f"\n{'📝 EXAMPLE 2: Without Verification (Caching Test)':<60}")
    config_no_verification = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=100,
        max_retries=3,
        max_concurrent_requests=5,
        # No verification callback - should use cache directly
    )
    
    # Use same prompts to test caching without verification
    run_batch(
        config=config_no_verification,
        cache_dir=cache_dir,
        force=False,
        run_label="No Verification (Should Use Cache)",
        prompts=mixed_prompts[:2],  # Use first 2 prompts
    )

    # Example 3: File-based Processing
    print(f"\n{'📁 EXAMPLE 3: File-based Processing':<60}")
    prompts_dir = "example_prompts"
    os.makedirs(prompts_dir, exist_ok=True)

    example_files = {
        "france": "What is the capital of France and what is it famous for?",
        "math": "Explain the concept of prime numbers with examples.",
        "shakespeare": "Who was William Shakespeare and why is he important?",
        "science": "What is gravity and how does it work?",
    }

    print(f"📂 Creating {len(example_files)} prompt files in '{prompts_dir}/'")
    for filename, content in example_files.items():
        filepath = os.path.join(prompts_dir, f"{filename}.txt")
        with open(filepath, "w") as f:
            f.write(content)
        print(f"   ✅ {filename}.txt")

    # Process files
    run_batch(
        config=config_no_verification,  # Use config without verification for speed
        cache_dir=cache_dir,
        force=False,
        run_label="File-based Processing",
        input_dir=prompts_dir,
    )

    # Example 4: Force Regeneration
    print(f"\n{'🔄 EXAMPLE 4: Force Regeneration':<60}")
    print("This will ignore cache and regenerate responses...")
    
    force_prompts = [
        "What is artificial intelligence? Be creative.",
        {"id": "force_test", "text": "Explain machine learning in simple terms."}
    ]
    
    run_batch(
        config=config_no_verification,
        cache_dir=cache_dir,
        force=True,  # Force regeneration
        run_label="Force Regeneration Test",
        prompts=force_prompts,
    )

    print(f"\n{'🎯 EXAMPLE COMPLETED':<60}")
    print("✅ All examples completed successfully!")
    print(f"📁 Check the '{cache_dir}' directory for cached responses")
    print(f"📁 Check the '{prompts_dir}' directory for example prompt files")
    print("\n🔍 Try running this script again to see caching in action!")


if __name__ == "__main__":
    main()
