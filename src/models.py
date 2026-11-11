"""Data models shared between the pipeline stages."""

from pathlib import Path
from collections import defaultdict
from langchain_core.documents import Document
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)


class Chunk:
    """A piece of a source file, with its position in the original."""

    def __init__(self, directory: str = "", chunk_size: int = 2000):
        """Initialize the chunker with splitters."""
        self.directory = directory
        self._chunk_size = chunk_size
        self._doc_chunk_overlap = 0
        self._code_chunk_overlap = 0

        self.splitter_md = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._doc_chunk_overlap,
            separators=["\n# ", ".\n", "\n", " ", ""],
            add_start_index=True,
        )
        # this one for python code
        self.splitter_code = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=self._chunk_size,
            chunk_overlap=self._code_chunk_overlap,
            add_start_index=True,
        )

    @staticmethod
    def safe_read(path: Path) -> str | None:
        """Read a text file as UTF-8. Returns None if unreadable. Never raises."""
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None

    # ---- 4 spaces — back at class level ----

    def load_documents(self, paths: list[str]) -> list[Document]:
        """Load files and create Documents with source metadata."""
        my_doc_list: list[Document] = []
        for file_path in paths:
            page_content = self.safe_read(Path(file_path))
            if not page_content or not page_content.strip():
                continue
            p = Path(file_path)
            my_doc_list.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "source": str(p),
                        "file_name": p.name,
                        "suffix": p.suffix,
                    },
                )
            )
        return my_doc_list

    def chunk_code(self, documents: list[Document]) -> list[Document]:
        """Split Python documents into code chunks."""
        return self.splitter_code.split_documents(documents)

    def chunk_docs(self, documents: list[Document]) -> list[Document]:
        """Split Markdown and text documents into chunks."""
        return self.splitter_md.split_documents(documents)

    def chunk_all(
        self,
        code_paths: list[str],
        doc_paths: list[str],
    ) -> list[Document]:
        """Process all code and documentation files."""
        code_chunks = self.chunk_code(self.load_documents(code_paths))
        doc_chunks = self.chunk_docs(self.load_documents(doc_paths))
        # print(doc_chunks[9])
        # print(doc_chunks[9].metadata.get("start_index", 0))
        # print(doc_chunks[9].metadata.get("start_index", 0) + len(doc_chunks[9].page_content))
        grouped = defaultdict(list)
        for chunk in code_chunks + doc_chunks:
            grouped[chunk.metadata["source"]].append(chunk)
        return dict(grouped)

    def get_chunk_count(self, chunks: list[Document]) -> int:
        """Return the total number of generated chunks."""
        return len(chunks)