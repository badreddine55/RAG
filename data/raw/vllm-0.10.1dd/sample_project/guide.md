# RAG Test Guide

This project demonstrates document discovery, chunking, and persistent indexing.

## Discovery

The parser finds supported source files recursively. Python files are treated as code, while Markdown and reStructuredText are treated as documentation.

## Chunking

Each document is split into smaller pieces. Every chunk keeps its source path and starting character index in metadata. The chunk size is measured in characters.

## Indexing

The index stores each file's modification timestamp and the generated chunks. A later run should skip unchanged files, process new or modified files, and remove deleted files.

## Verification

Run the indexer twice. The first run should report new files. The second run should report unchanged files. Then edit one file and verify that it is classified as modified.
