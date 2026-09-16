from io import BytesIO

from docx import Document
from pypdf import PdfReader

def extract_text(file_name: str, content : bytes):
    extension = file_name.lower().split(".")[-1]

    if extension == "txt":
        return content.decode("utf-8")

    if extension == "pdf":
        reader = PdfReader(BytesIO(content))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    if extension == "docx":
        document = Document(BytesIO(content))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    raise ValueError(
        f"Unsupported file type: .{extension}"
    )