from pathlib import Path

class Parccer():
    
    def __init__(self):
        self.code_files: list[str] = []
        self.doc_files: list[str] = []
        self.code_ext = {".py"}
        self.doc_ext = {".md", ".txt",".rst"}
        self.ignored_dirs = {"__pycache__", ".git", ".venv", "node_modules"}

    def load_files(self, root: str | Path) -> tuple[list[str], list[str]]:
        """Find the files to index under a root directory.

        Args:
            root: Directory to scan, e.g. "data/raw".
        Returns:
            A tuple (code_files, doc_files) of sorted path strings.
        """
        root_path = Path(root)
        if not root_path.is_dir():
            raise FileNotFoundError(f"Not a directory: {root_path}")
        for path in sorted(root_path.rglob("*")):
            if not path.is_file():
                continue
            if self.ignored_dirs.intersection(path.parts):
                continue
            suffix = path.suffix.lower()
            if suffix in self.code_ext:
                self.code_files.append(path.as_posix())
            elif suffix in self.doc_ext:
                self.doc_files.append(path.as_posix())

        return self.code_files, self.doc_files