import hashlib
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


def read_prompt_files(input_dir: str) -> List[Tuple[str, str]]:
    """Read all text files from input directory and return as (filename, content) pairs.

    Args:
        input_dir: Path to directory containing prompt files

    Returns:
        List of (prompt_id, prompt_text) tuples where prompt_id is the filename without extension
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise ValueError(f"Input directory {input_dir} does not exist")

    prompts = []
    for file_path in input_path.glob("*.txt"):
        with open(file_path, "r") as f:
            content = f.read().strip()
            # Use filename without extension as prompt_id
            prompt_id = file_path.stem
            prompts.append((prompt_id, content))

    if not prompts:
        raise ValueError(f"No .txt files found in {input_dir}")

    return prompts


def read_prompt_list(
    input_source: List[Union[str, Tuple[str, str], Dict[str, Any]]],
) -> List[Tuple[str, str]]:
    """Read prompts from a list of various formats.

    Args:
        input_source: List of prompts in any of these formats:
            - str: The prompt text (will use hash as ID)
            - tuple: (prompt_id, prompt_text)
            - dict: {"id": prompt_id, "text": prompt_text}

    Returns:
        List of (prompt_id, prompt_text) tuples
    """
    prompts = []
    for item in input_source:
        if isinstance(item, str):
            # String format: use hash as ID
            prompt_id = hashlib.sha256(item.encode()).hexdigest()[:32]
            prompt_text = item
        elif isinstance(item, tuple) and len(item) == 2:
            # Tuple format: (prompt_id, prompt_text)
            prompt_id, prompt_text = item
        elif isinstance(item, dict) and "id" in item and "text" in item:
            # Dict format: {"id": prompt_id, "text": prompt_text}
            prompt_id = item["id"]
            prompt_text = item["text"]
        else:
            raise ValueError(f"Invalid prompt format: {item}")
        prompts.append((prompt_id, prompt_text))
    return prompts


def get_prompts(
    input_source: Union[str, List[Union[str, Tuple[str, str], Dict[str, Any]]]],
) -> List[Tuple[str, str]]:
    """Get prompts from either a directory or a list.

    Args:
        input_source: Either:
            - str: Path to directory containing prompt files
            - List: List of prompts in various formats (string, tuple, or dict)

    Returns:
        List of (prompt_id, prompt_text) tuples
    """
    if isinstance(input_source, str):
        return read_prompt_files(input_source)
    elif isinstance(input_source, list):
        return read_prompt_list(input_source)
    else:
        raise ValueError(f"Invalid input source type: {type(input_source)}")
