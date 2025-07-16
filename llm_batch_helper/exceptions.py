class VerificationFailedError(Exception):
    """Custom exception for when verification callback fails."""

    def __init__(self, message, prompt_id, llm_response_data=None):
        super().__init__(message)
        self.prompt_id = prompt_id
        self.llm_response_data = llm_response_data
