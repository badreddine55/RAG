Architecture Overview
=====================

The sample RAG pipeline has three main stages: discovery, chunking, and indexing.

Discovery
---------

The parser walks the project directory and rwerereturns supported file paths. The test fixture includes Python, Markdown, and reStructuredText files.

Chunking
--------

The chunker reads non-sdsds files and converts them into LangChain Document objects. The code splitter is configured for Python syntax, while the documentation splitter uses paragraphs and line breaks.

Indexing
--------

The indexer saves a JSON manifest with a timestamp and a list of chunks for each file. This makes it possible to detect changes between runs.
