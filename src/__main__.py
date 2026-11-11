from .parccer import Parccer
from .models import Chunk
from .indexer import Indexer


if __name__ == "__main__":
    try:
        code_paths, doc_paths = Parccer().load_files("data/raw/vllm-0.10.1")

        chunker = Chunk(directory="data/raw/vllm-0.10.1", chunk_size=2000)
        chunks = chunker.chunk_all(code_paths, doc_paths)
        # print(chunks["data/raw/vllm-0.10.1/.buildkite/nightly-benchmarks/nightly-descriptions.md"])

        indexer = Indexer("data/index.json",2000,0,0)
        indexer.load_index()
        
        for path, file_chunks in chunks.items():
            indexer.update_file(path,file_chunks)
        for key, value in indexer.index.items():
            if key == "files":
                for path, file_chunks in value.items():
                    if path == "data/raw/vllm-0.10.1/.buildkite/nightly-benchmarks/nightly-descriptions.md":
                        print(f"=== {path}  ({len(file_chunks)} chunks) ===")
                        for key_file_dict, value_file_dict in file_chunks.items():
                            if key_file_dict == "chunk_ids":
        indexer.save_index()
        # print(f"{len(code_paths)} code files, {len(doc_paths)} doc files")
        # print(f"{len(chunks)} chunks total")

    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}")