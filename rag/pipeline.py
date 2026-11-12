import os

from rag.loader import load_pdf
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.retriever import Retriever
from rag.vector_store import (
    save_vector_store,
    load_vector_store
)
from rag.document import get_document_hash


VECTORSTORE_ROOT = "vectorstore"


def get_vectorstore_path(pdf_path):

    document_hash = get_document_hash(pdf_path)

    vectorstore_dir = os.path.join(
        VECTORSTORE_ROOT,
        document_hash
    )

    return vectorstore_dir


def build_knowledge_base(pdf_path):

    vectorstore_dir = get_vectorstore_path(
        pdf_path
    )

    index_path = os.path.join(
        vectorstore_dir,
        "index.faiss"
    )

    chunks_path = os.path.join(
        vectorstore_dir,
        "chunks.pkl"
    )

    # ------------------------------------------
    # CHECK IF DOCUMENT IS ALREADY INDEXED
    # ------------------------------------------

    if (
        os.path.exists(index_path)
        and os.path.exists(chunks_path)
    ):

        print("Loading existing vector store...")

        index, chunks = load_vector_store(
            vectorstore_dir
        )

        retriever = Retriever.from_index(
            index,
            chunks
        )

        print("Vector store loaded!")

        return retriever

    # ------------------------------------------
    # BUILD NEW VECTOR STORE
    # ------------------------------------------

    print("Building vector store...")

    print("Loading PDF...")

    pages = load_pdf(pdf_path)

    print(
        "Number of pages:",
        len(pages)
    )

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print(
        "Number of chunks:",
        len(chunks)
    )

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print(
        "Embeddings shape:",
        embeddings.shape
    )

    print("Creating FAISS index...")

    retriever = Retriever(
        embeddings,
        chunks
    )

    save_vector_store(
        retriever.index,
        chunks,
        vectorstore_dir
    )

    print("Knowledge base created!")

    return retriever