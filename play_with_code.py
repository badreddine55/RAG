from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
)

code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b
"""

text = """
Python is a popular programming language used for web development,
artificial intelligence, automation, and data analysis.

Many developers enjoy Python because its syntax is simple and easy
to understand. It allows programmers to build complex applications
with relatively little code.

Artificial intelligence is changing the way people interact with
technology. Machine learning models can analyze large amounts of
information and recognize patterns in data.

One interesting application of artificial intelligence is the
development of intelligent search systems. These systems can
understand questions and retrieve relevant information from
large collections of documents.

Retrieval-Augmented Generation, also known as RAG, combines
information retrieval with language models. Instead of relying
only on previously learned knowledge, a RAG system searches
external documents before generating an answer.

When working with large documents, developers often divide
the text into smaller sections called chunks. Each chunk
contains a portion of the original document.

Choosing the right chunk size is important because very small
chunks may lose useful context, while very large chunks may
contain too much unrelated information.

Software engineering also requires testing, debugging, and
maintaining clean code. Developers frequently collaborate
on projects using version control systems such as Git.
"""

# splitter = RecursiveCharacterTextSplitter.from_language(
#     language=Language.PYTHON,
#     chunk_size=80,
#     chunk_overlap=20,
#     add_start_index=True,
# )

chunks = splitter.create_documents([code])

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)

    
splitter_md = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=0,
            separators=["\n## ", "\n# ", "\n\n", "\n", " ", ""],
            add_start_index=True
        )

for name in dir(splitter_md):
    if not name.startswith("_"):
        print(name)

# for i, chunk in enumerate(chunks):
#     print(f"\n--- Chunk {i + 1} ---")
#     print(chunk.page_content)
#     print("Metadata:", chunk.metadata)