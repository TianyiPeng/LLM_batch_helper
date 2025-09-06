from typing import Callable, Dict, Optional

# System instruction for Gemini
SYSTEM_INSTRUCTION = """You are a helpful AI assistant. """


class LLMConfig:
    def __init__(
        self,
        model_name: str,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
        max_retries: int = 5,  # Max retries for the combined LLM call + Verification
        max_concurrent_requests: int = 30,
        verification_callback: Optional[Callable[..., bool]] = None,
        verification_callback_args: Optional[Dict] = None,
        max_completion_tokens: Optional[int] = None,
        **kwargs
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_completion_tokens = max_completion_tokens
        if self.max_tokens and not self.max_completion_tokens:
            self.max_completion_tokens = self.max_tokens
        self.system_instruction = system_instruction or SYSTEM_INSTRUCTION
        self.max_retries = max_retries
        self.max_concurrent_requests = max_concurrent_requests
        self.verification_callback = verification_callback
        self.verification_callback_args = (
            verification_callback_args if verification_callback_args is not None else {}
        )
        self.kwargs = kwargs