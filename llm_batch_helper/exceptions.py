class VerificationFailedError(Exception):
    """Custom exception for when verification callback fails."""

    def __init__(self, message, prompt_id, llm_response_data=None):
        super().__init__(message)
        self.prompt_id = prompt_id
        self.llm_response_data = llm_response_data


class InvalidPromptFormatError(Exception):
    """Custom exception for invalid prompt format."""

    def __init__(self, message, invalid_item=None):
        super().__init__(message)
        self.invalid_item = invalid_item
