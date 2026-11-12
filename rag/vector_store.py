import faiss
import pickle
import os


def save_vector_store(index, chunks, vectorstore_dir):
    os.makedirs(vectorstore_dir, exist_ok=True)

    index_path = os.path.join(
        vectorstore_dir,
        "index.faiss"
    )

    chunks_path = os.path.join(
        vectorstore_dir,
        "chunks.pkl"
    )

    faiss.write_index(index, index_path)

    with open(chunks_path, "wb") as file:
        pickle.dump(chunks, file)


def load_vector_store(vectorstore_dir):
    index_path = os.path.join(
        vectorstore_dir,
        "index.faiss"
    )

    chunks_path = os.path.join(
        vectorstore_dir,
        "chunks.pkl"
    )

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as file:
        chunks = pickle.load(file)

    return index, chunks