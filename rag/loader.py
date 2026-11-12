import pymupdf
import html
import re


def clean_text(text):

    # Decode HTML entities such as &#x20;
    text = html.unescape(text)

    # Replace multiple whitespace characters with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def load_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        text = clean_text(text)

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages