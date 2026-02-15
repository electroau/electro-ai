from __future__ import annotations

from io import BytesIO

import pandas as pd
import pdfplumber


def parse_document(file_type: str, payload: bytes) -> str:
    if file_type == 'pdf':
        return _parse_pdf(payload)
    if file_type == 'csv':
        return _parse_csv(payload)
    if file_type == 'xlsx':
        return _parse_xlsx(payload)
    raise ValueError(f'Unsupported file type: {file_type}')


def normalize_text(text: str) -> str:
    return ' '.join(text.replace('\x00', ' ').split())


def chunk_text(text: str, max_tokens: int = 800) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    for i in range(0, len(words), max_tokens):
        chunks.append(' '.join(words[i : i + max_tokens]))
    return chunks


def _parse_pdf(payload: bytes) -> str:
    text_pages: list[str] = []
    with pdfplumber.open(BytesIO(payload)) as pdf:
        for page in pdf.pages:
            text_pages.append(page.extract_text() or '')
    return normalize_text('\n'.join(text_pages))


def _parse_csv(payload: bytes) -> str:
    df = pd.read_csv(BytesIO(payload))
    return normalize_text(df.to_json(orient='records'))


def _parse_xlsx(payload: bytes) -> str:
    sheets = pd.read_excel(BytesIO(payload), sheet_name=None)
    normalized_sheets = []
    for sheet_name, frame in sheets.items():
        normalized_sheets.append(f'{sheet_name}: {frame.to_json(orient="records")}')
    return normalize_text('\n'.join(normalized_sheets))
