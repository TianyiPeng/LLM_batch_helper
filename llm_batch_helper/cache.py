import json
from pathlib import Path
from typing import Any, Dict, Optional


class LLMCache:
    def __init__(self, cache_dir: str = "llm_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, prompt_id: str) -> Path:
        """Generate cache file path based on prompt_id."""
        return self.cache_dir / f"{prompt_id}.json"

    def get_cached_response(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if it exists."""
        cache_path = self._get_cache_path(prompt_id)
        if cache_path.exists():
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    def save_response(self, prompt_id: str, prompt: str, response: Dict[str, Any]) -> None:
        """Save response to cache."""
        cache_path = self._get_cache_path(prompt_id)
        cache_data = {"prompt_input": prompt, "llm_response": response}
        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)

    def clear_cache(self) -> None:
        """Clear all cached responses."""
        if self.cache_dir.exists():
            for file in self.cache_dir.glob("*.json"):
                file.unlink()
