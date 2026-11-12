from rag.pipeline import build_knowledge_base
from rag.embeddings import model
from rag.reranker import rerank_results
from rag.generator import generate_answer


# ==========================================
# BUILD KNOWLEDGE BASE
# ==========================================

pdf_path = "data/annual_report.pdf"

retriever = build_knowledge_base(
    pdf_path
)


# ==========================================
# ASK QUESTION
# ==========================================

question = input(
    "\nAsk FinSight a question: "
)


# ==========================================
# EMBED QUESTION
# ==========================================

query_embedding = model.encode(
    [question],
    convert_to_numpy=True,
    normalize_embeddings=True
)


# ==========================================
# RETRIEVE CANDIDATES
# ==========================================

results = retriever.search(
    query_embedding,
    k=10
)


# ==========================================
# RERANK
# ==========================================

stop_words = {
    "what", "are", "the", "is", "a",
    "an", "of", "in", "for", "to",
    "how", "did", "was", "were"
}

keywords = [
    word.lower().strip("?,.!'\"")
    for word in question.split()
    if word.lower().strip("?,.!'\"")
    not in stop_words
]

results = rerank_results(
    results,
    keywords,
    top_k=5
)


# ==========================================
# DISPLAY SOURCES
# ==========================================

print("\n===== RETRIEVED SOURCES =====")

for result in results:

    print("\n--------------------")
    print("Page:", result["page"])
    print("Similarity:", round(result["score"], 4))
    print(result["text"][:500])


# ==========================================
# GENERATE ANSWER
# ==========================================

answer = generate_answer(
    question,
    results
)


# ==========================================
# DISPLAY ANSWER
# ==========================================

print("\n===== FINSIGHT ANSWER =====")

print(answer)