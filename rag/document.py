import hashlib


def get_document_hash(pdf_path):

    sha256 = hashlib.sha256()

    with open(pdf_path, "rb") as file:

        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()