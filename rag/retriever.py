import faiss
import numpy as np


class Retriever:

    def __init__(self, embeddings, chunks):

        self.chunks = chunks

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(
            embeddings.astype("float32")
        )

    @classmethod
    def from_index(cls, index, chunks):

        retriever = cls.__new__(cls)

        retriever.index = index
        retriever.chunks = chunks

        return retriever

    def search(self, query_embedding, k=5):

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            results.append({
                "text": self.chunks[index]["text"],
                "page": self.chunks[index]["page"],
                "score": float(distance)
            })

        return results