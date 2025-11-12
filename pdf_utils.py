from io import BytesIO
from pypdf import PdfReader

def pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    text = []
    for page in reader.pages:
        try:
            content = page.extract_text()
            if content:
                text.append(content.strip())
        except Exception:
            continue
    return "\n\n".join(text)
