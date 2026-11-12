def rerank_results(results, keywords, top_k=5):

    scored_results = []

    for result in results:

        text = result["text"].lower()

        keyword_score = sum(
            1 for keyword in keywords
            if keyword.lower() in text
        )

        combined_score = (
            result["score"] + (keyword_score * 0.05)
        )

        result["rerank_score"] = combined_score

        scored_results.append(result)

    scored_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return scored_results[:top_k]