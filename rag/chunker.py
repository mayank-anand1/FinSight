def create_chunks(pages, chunk_size=1200, overlap=200):

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            # Try to end the chunk at a sentence boundary
            if end < len(text):

                sentence_end = text.rfind(".", start, end)

                if sentence_end > start + 600:
                    end = sentence_end + 1

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "page": page["page"]
                })

            start = end - overlap

    return chunks