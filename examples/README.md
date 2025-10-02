# LLM Batch Helper Examples

This directory contains examples demonstrating the key features of the `llm_batch_helper` package.

## Available Examples

### 📝 `example.py` - Prompt Mode Features
Demonstrates traditional prompt-based processing with:
- Multiple input formats (string, tuple, dictionary)
- File-based prompt processing
- Custom verification callbacks
- Caching functionality
- Error handling and retry logic

### 💬 `example_message.py` - Message Mode Features ⭐ NEW!
Demonstrates the new conversation-based processing with:
- Multi-turn conversation handling
- System, user, and assistant message roles
- Mixed conversation lengths in batches
- Dictionary and tuple message formats
- Conversation caching and verification
- Error handling for message validation

## Directory Structure

```
examples/
├── README.md                   # This file
├── example.py                  # Prompt mode examples
├── example_message.py          # Message mode examples (NEW!)
├── example_prompts/           # Sample prompt files
│   ├── france.txt
│   ├── math.txt
│   └── shakespeare.txt
```

## Setup and Running

### 1. Set up API Keys

For **OpenAI** (used in `example.py`):
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

For **OpenRouter** (used in `example_message.py`):
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
```

For **Other Providers**:
```bash
export TOGETHER_API_KEY="your-together-api-key"     # Together.ai
export GEMINI_API_KEY="your-gemini-api-key"         # Google Gemini
```

### 2. Run the Examples

**Traditional Prompt Mode:**
```bash
cd examples
python example.py
```

**New Message Mode:**
```bash
cd examples  
python example_message.py
```

## Example Features Demonstrated

### Prompt Mode (`example.py`)
- ✅ String prompts with auto-generated IDs
- ✅ Tuple format: `("custom_id", "prompt_text")`
- ✅ Dictionary format: `{"id": "custom_id", "text": "prompt_text"}`
- ✅ File-based processing from text files
- ✅ Custom verification callbacks
- ✅ Response caching and cache validation
- ✅ Force regeneration capabilities
- ✅ Error handling and retry mechanisms

### Message Mode (`example_message.py`)
- 💬 Multi-turn conversations with context
- 🎭 System, user, and assistant message roles
- 📋 Tuple format: `("message_id", [message_list])`
- 📋 Dictionary format: `{"id": "message_id", "messages": [message_list]}`
- 🔄 Mixed conversation lengths in single batch
- 💾 Conversation-aware caching
- ✅ Message format validation
- 🚫 Input mode conflict prevention

## Key Differences: Prompt vs Message Mode

| Feature | Prompt Mode | Message Mode |
|---------|-------------|--------------|
| **Input** | Single prompts | Multi-turn conversations |
| **Context** | System instruction + user prompt | Full conversation history |
| **Use Cases** | Q&A, independent tasks | Chat, tutorials, ongoing assistance |
| **Format** | `prompts=[...]` | `messages=[...]` |
| **Caching** | By prompt content | By conversation context |

## Customizing the Examples

### Adding Your Own Prompts
1. Create text files in `example_prompts/` directory
2. Each file should contain a single prompt
3. The filename (without `.txt`) becomes the prompt ID
4. Run `example.py` to process them

### Creating Your Own Conversations
1. Define conversations in the message format:
   ```python
   messages = [
       ("conversation_id", [
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": "Hello!"},
           {"role": "assistant", "content": "Hi! How can I help?"},
           {"role": "user", "content": "Tell me about Python."}
       ])
   ]
   ```
2. Process with `process_prompts_batch(messages=messages, ...)`

### Force Cache Regeneration
```python
# Regenerate all responses
results = process_prompts_batch(
    prompts=your_prompts,  # or messages=your_messages
    config=config,
    force=True  # Ignore cache
)
```



Happy batch processing! 🚀 