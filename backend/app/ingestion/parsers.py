from io import BytesIO
import pandas as pd
from pypdf import PdfReader


def parse_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def parse_excel(content: bytes) -> str:
    sheets = pd.read_excel(BytesIO(content), sheet_name=None)
    parts: list[str] = []
    for sheet_name, frame in sheets.items():
        parts.append(f"# {sheet_name}")
        parts.append(frame.to_csv(index=False))
    return "\n".join(parts)
