"""
LLM Batch Helper Message Mode Example Script

This example demonstrates the new message mode features of LLM Batch Helper:
- Multi-turn conversation processing
- Message format support (tuple and dictionary)
- Conversation history handling
- System, user, and assistant message roles
- Caching with conversation contexts
- Mixed conversation lengths in batches

🎉 New in v0.4.0: Message Mode Support!
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the package
sys.path.append(str(Path(__file__).parent.parent))
from llm_batch_helper import LLMConfig, process_prompts_batch, get_messages


def example_conversation_verification(
    message_id: str, llm_response_data: dict, original_message_text: str, **kwargs
) -> bool:
    """Example verification callback for conversation responses."""
    response_text = llm_response_data.get("response_text", "")
    min_length = kwargs.get("min_length", 5)
    
    if not response_text.strip():
        print(f"❌ Verification failed for {message_id}: Empty response")
        return False
    
    if len(response_text) < min_length:
        print(f"❌ Verification failed for {message_id}: Too short ({len(response_text)} < {min_length})")
        return False
    
    # Check for inappropriate responses (simple example)
    inappropriate_phrases = ["I can't", "I'm not able", "I cannot"]
    if any(phrase in response_text for phrase in inappropriate_phrases):
        print(f"⚠️  Flagged response for {message_id}: May need review")
    
    print(f"✅ Verification passed for {message_id}")
    return True


def run_message_batch(config, cache_dir, force, run_label, **kwargs):
    """Helper function to run a message batch and display results."""
    print(f"\n{'='*60}")
    print(f"💬 {run_label}")
    print(f"   Cache: {cache_dir} | Force: {force}")
    print(f"{'='*60}")
    
    # Process messages using the new message mode
    results = process_prompts_batch(
        config=config,
        provider="openrouter",  # Using OpenRouter for variety
        desc=f"{run_label}",
        cache_dir=cache_dir,
        force=force,
        **kwargs,
    )
    
    # Display results with conversation context
    successful = 0
    cached = 0
    failed = 0
    
    for message_id, response in results.items():
        if "error" in response:
            status = "❌ [ERROR]"
            print(f"{status} {message_id}: {response['error'][:100]}...")
            failed += 1
        elif response.get("from_cache"):
            status = "💾 [CACHE]"
            print(f"{status} {message_id}:")
            print(f"    💬 {response['response_text'][:120]}...")
            cached += 1
            successful += 1
        else:
            status = "✅ [NEW]"
            print(f"{status} {message_id}:")
            print(f"    💬 {response['response_text'][:120]}...")
            successful += 1
    
    print(f"\n📊 Summary: {successful} successful ({cached} cached), {failed} failed")


def main():
    """Main example function demonstrating message mode features."""
    print("💬 LLM Batch Helper Message Mode Example")
    print("Demonstrating multi-turn conversations and message processing!")
    
    cache_dir = "message_cache"
    
    # Configuration for message processing
    print(f"\n{'🔧 CONFIGURATION':<60}")
    config = LLMConfig(
        model_name="openai/gpt-4o-mini",  # Using OpenRouter format
        temperature=0.7,
        max_completion_tokens=150,
        max_retries=2,
        max_concurrent_requests=3,
        verification_callback=example_conversation_verification,
        verification_callback_args={"min_length": 10},
    )
    
    print(f"✅ Created config for message mode")
    print(f"   Model: {config.model_name}")
    print(f"   Provider: OpenRouter")
    print(f"   Max concurrent: {config.max_concurrent_requests}")
    
    # Example 1: Multi-turn Conversations
    print(f"\n{'💬 EXAMPLE 1: Multi-turn Conversations':<60}")
    conversation_messages = [
        # Math tutoring conversation
        ("math_tutor", [
            {"role": "system", "content": "You are a helpful math tutor. Be encouraging and clear."},
            {"role": "user", "content": "I'm struggling with algebra. What's a quadratic equation?"},
            {"role": "assistant", "content": "A quadratic equation is a polynomial equation of degree 2, typically written as ax² + bx + c = 0."},
            {"role": "user", "content": "Can you give me a simple example and show how to solve it?"}
        ]),
        
        # Creative writing assistant
        ("creative_writer", [
            {"role": "system", "content": "You are a creative writing assistant. Be imaginative and inspiring."},
            {"role": "user", "content": "I want to write a short story about time travel."},
            {"role": "assistant", "content": "Time travel stories are fascinating! Consider these elements: the mechanism of travel, the consequences of changing the past, and the emotional journey of your protagonist."},
            {"role": "user", "content": "What if my character accidentally changes something small but it has huge consequences?"}
        ]),
        
        # Simple Q&A
        ("quick_fact", [
            {"role": "user", "content": "What's the tallest mountain in the world and how tall is it?"}
        ])
    ]
    
    run_message_batch(
        config=config,
        cache_dir=cache_dir,
        force=False,
        run_label="Multi-turn Conversations",
        messages=conversation_messages,
    )

    # Example 2: Dictionary Format Messages
    print(f"\n{'📋 EXAMPLE 2: Dictionary Format Messages':<60}")
    dict_format_messages = [
        {
            "id": "tech_support",
            "messages": [
                {"role": "system", "content": "You are a helpful tech support agent. Be patient and thorough."},
                {"role": "user", "content": "My computer is running slowly. What could be wrong?"},
                {"role": "assistant", "content": "Slow computer performance can have several causes. Let's start with the basics: How much free storage space do you have?"},
                {"role": "user", "content": "I have about 5GB free out of 256GB total."}
            ]
        },
        {
            "id": "language_practice",
            "messages": [
                {"role": "system", "content": "You are a language learning assistant. Help users practice Spanish."},
                {"role": "user", "content": "Can you help me practice ordering food in Spanish?"},
                {"role": "assistant", "content": "¡Por supuesto! Here are some useful phrases: 'Quisiera...' (I would like...), '¿Qué recomienda?' (What do you recommend?)"},
                {"role": "user", "content": "How do I say 'I'm allergic to nuts' in Spanish?"}
            ]
        }
    ]
    
    run_message_batch(
        config=config,
        cache_dir=cache_dir,
        force=False,
        run_label="Dictionary Format Messages",
        messages=dict_format_messages,
    )

    # Example 3: Mixed Conversation Lengths
    print(f"\n{'📏 EXAMPLE 3: Mixed Conversation Lengths':<60}")
    mixed_length_messages = [
        # Single user message
        ("single_turn", [
            {"role": "user", "content": "Explain photosynthesis in one sentence."}
        ]),
        
        # Two-turn conversation
        ("two_turn", [
            {"role": "user", "content": "What's the weather like on Mars?"},
            {"role": "assistant", "content": "Mars has a cold, dry climate with temperatures averaging around -80°F (-62°C) and frequent dust storms."},
            {"role": "user", "content": "Could humans survive there without a spacesuit?"}
        ]),
        
        # Longer conversation with system prompt
        ("detailed_help", [
            {"role": "system", "content": "You are an expert chef. Provide clear, step-by-step cooking instructions."},
            {"role": "user", "content": "I want to make pasta from scratch but I'm a beginner."},
            {"role": "assistant", "content": "Making fresh pasta is rewarding! You'll need flour, eggs, and a bit of olive oil. Start with 100g flour per egg."},
            {"role": "user", "content": "What type of flour should I use?"},
            {"role": "assistant", "content": "For beginners, use '00' flour if available, or all-purpose flour works fine. The key is kneading well."},
            {"role": "user", "content": "How long should I knead the dough?"}
        ])
    ]
    
    run_message_batch(
        config=config,
        cache_dir=cache_dir,
        force=False,
        run_label="Mixed Conversation Lengths",
        messages=mixed_length_messages,
    )

    # Example 4: Testing Message Processing Function
    print(f"\n{'🔧 EXAMPLE 4: Message Processing Function':<60}")
    test_messages = [
        ("test_tuple", [{"role": "user", "content": "Hello world!"}]),
        {"id": "test_dict", "messages": [{"role": "user", "content": "Testing dictionary format"}]}
    ]
    
    try:
        processed = get_messages(test_messages)
        print(f"✅ get_messages() processed {len(processed)} messages successfully")
        for msg_id, msg_list in processed:
            print(f"   📧 {msg_id}: {len(msg_list)} message(s)")
    except Exception as e:
        print(f"❌ get_messages() failed: {e}")

    # Example 5: Caching Test (Re-run same conversations)
    print(f"\n{'💾 EXAMPLE 5: Caching Test':<60}")
    print("Running the same conversations again to test caching...")
    
    config_no_verification = LLMConfig(
        model_name="openai/gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=150,
        max_retries=2,
        max_concurrent_requests=3,
        # No verification callback to test direct cache usage
    )
    
    run_message_batch(
        config=config_no_verification,
        cache_dir=cache_dir,
        force=False,
        run_label="Caching Test (Should Use Cache)",
        messages=conversation_messages[:2],  # Use first 2 conversations
    )

    # Example 6: Error Handling Demo
    print(f"\n{'⚠️  EXAMPLE 6: Error Handling Demo':<60}")
    try:
        # This should fail validation
        invalid_messages = [
            ("invalid", "not a list")  # Wrong format
        ]
        get_messages(invalid_messages)
        print("❌ Should have failed validation")
    except Exception as e:
        print(f"✅ Properly caught invalid format: {str(e)[:60]}...")
    
    try:
        # This should fail multiple input validation
        process_prompts_batch(
            prompts=["test"],
            messages=[("test", [{"role": "user", "content": "test"}])],
            config=config,
            provider="openrouter"
        )
        print("❌ Should have failed multiple input validation")
    except ValueError as e:
        print(f"✅ Properly caught multiple inputs: {str(e)[:60]}...")

    print(f"\n{'🎯 MESSAGE MODE EXAMPLES COMPLETED':<60}")
    print("✅ All message mode examples completed successfully!")
    print(f"📁 Check the '{cache_dir}' directory for cached conversation responses")
    print("\n🔍 Key takeaways from message mode:")
    print("   💬 Support for multi-turn conversations")
    print("   🎭 System, user, and assistant roles")
    print("   📋 Flexible input formats (tuple and dictionary)")
    print("   💾 Full caching support for conversations")
    print("   ⚡ Same performance benefits as prompt mode")
    print("   🔧 Compatible with all existing features")
    print("\n🚀 Try mixing different conversation types in your own applications!")


if __name__ == "__main__":
    main()