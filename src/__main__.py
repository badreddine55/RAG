
from pathlib import Path

from .parccer import Parccer
from .models import Chunk
from .indexer import Indexer


if __name__ == "__main__":
    try:
        directory = "data/raw/vllm-0.10.1"
        chunk_size = 2000

        code_paths, doc_paths = Parccer().load_files(directory)

        chunker = Chunk(
            directory=directory,
            chunk_size=chunk_size,
        )

        indexer = Indexer(
            "data/index.json",
            chunk_size,
            0,
            0,
        )

        # Ignore empty files
        code_paths = [
            path for path in code_paths
            if Path(path).stat().st_size > 0
        ]

        doc_paths = [
            path for path in doc_paths
            if Path(path).stat().st_size > 0
        ]

        all_paths = code_paths + doc_paths

        changes = indexer.detect_changes(all_paths)

        if indexer.config_changed():
            print("Configuration changed. Rebuilding index...")

            # Build a fresh index in memory
            chunks = chunker.chunk_all(
                code_paths,
                doc_paths,
            )

            # Check that every non-empty file was processed
            missing = set(all_paths) - set(chunks)

            if missing:
                raise ValueError(
                    f"Cannot rebuild index: "
                    f"{len(missing)} files produced no chunks"
                )

            indexer.reset_index()

            for path, file_chunks in chunks.items():
                indexer.update_file(path, file_chunks)

        else:
            files_to_process = (
                changes["new"] + changes["modified"]
            )

            code_to_process = [
                path for path in files_to_process
                if path.endswith(".py")
            ]

            docs_to_process = [
                path for path in files_to_process
                if path.endswith((".md", ".txt", ".rst"))
            ]

            chunks = chunker.chunk_all(
                code_to_process,
                docs_to_process,
            )

            for path, file_chunks in chunks.items():
                indexer.update_file(path, file_chunks)

            for path in changes["deleted"]:
                indexer.index["files"].pop(path, None)

        indexer.save_index()

        print("New:", len(changes["new"]))
        print("Modified:", len(changes["modified"]))
        print("Deleted:", len(changes["deleted"]))
        print("Unchanged:", len(changes["unchanged"]))

    except (OSError, ValueError, TypeError) as err:
        print(f"Error: {err}")
