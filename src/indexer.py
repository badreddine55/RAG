
"""Manage the persistent index manifest for the RAG pipeline."""

import json
import os
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any


class Indexer:
    """Load, manage, and save the index dictionary."""

    def __init__(
        self,
        index_path: str = "data/index.json",
        chunk_size: int = 2000,
        code_overlap: int = 0,
        doc_overlap: int = 0,
    ) -> None:
        """Initialize the indexer and load the saved index."""
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if not 0 <= code_overlap < chunk_size:
            raise ValueError("Invalid code_overlap")

        if not 0 <= doc_overlap < chunk_size:
            raise ValueError("Invalid doc_overlap")

        self.index_path = Path(index_path)

        self.current_config = {
            "chunk_size": chunk_size,
            "code_overlap": code_overlap,
            "doc_overlap": doc_overlap,
        }

        self._default_index = {
            "config": deepcopy(self.current_config),
            "files": {},
        }

        self.index = self.load_index()

    def load_index(self) -> dict[str, Any]:
        """Load a saved index or return a new default index."""
        if not self.index_path.is_file():
            if self.index_path.exists():
                raise ValueError(
                    f"Index path is not a file: {self.index_path}"
                )
            return deepcopy(self._default_index)

        try:
            with self.index_path.open(
                "r", encoding="utf-8"
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as err:
            raise ValueError(
                f"Invalid JSON in {self.index_path}: {err}"
            ) from err

        except UnicodeError as err:
            raise ValueError(
                f"Invalid encoding in {self.index_path}: {err}"
            ) from err

        except OSError as err:
            raise OSError(
                f"Cannot read index {self.index_path}: {err}"
            ) from err

        if not isinstance(data, dict):
            raise ValueError("Index must be a dictionary")

        if not isinstance(data.get("config"), dict):
            raise ValueError("Missing or invalid index config")

        if not isinstance(data.get("files"), dict):
            raise ValueError("Missing or invalid index files")

        required_config = (
            "chunk_size",
            "code_overlap",
            "doc_overlap",
        )

        for key in required_config:
            value = data["config"].get(key)

            if type(value) is not int:
                raise ValueError(
                    f"Invalid configuration value: {key}"
                )

        saved_config = data["config"]

        size = saved_config["chunk_size"]

        if size <= 0:
            raise ValueError("Saved chunk_size must be positive")

        for key in ("code_overlap", "doc_overlap"):
            value = saved_config[key]

            if not 0 <= value < size:
                raise ValueError(
                    f"Invalid saved configuration: {key}"
                )

        for path, info in data["files"].items():
            if not isinstance(path, str):
                raise ValueError("File keys must be strings")

            if not isinstance(info, dict):
                raise ValueError(
                    f"Invalid file information: {path}"
                )

        return data

    def save_index(self) -> None:
        """Save the current index dictionary to JSON."""
        try:
            self.index_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with self.index_path.open("w", encoding="utf-8") as file:
                json.dump(self.index, file, indent=4)

        except (OSError, TypeError, ValueError) as err:
            raise OSError(f"Cannot save index: {err}") from err

        def config_changed(self) -> bool:
            """Check whether chunking configuration has changed."""
            return self.index["config"] != self.current_config

    def update_file(self,path: str,chunk_ids: list[str]) -> None:
        """Record an indexed file in the dictionary."""
        file_path = Path(path)

        self.index["files"][path] = {
            "mtime_ns": file_path.stat().st_mtime_ns,
            "chunk_ids": chunk_ids,
        }