from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)


def load_documents_from_dir(directory: str) -> List[Tuple[str, str]]:
    """Return list of (name, text) for all .txt/.pdf in directory."""
    base = Path(directory)
    docs: List[Tuple[str, str]] = []
    if not base.exists():
        return docs

    for path in base.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() == ".txt":
            text = read_text_file(path)
        elif path.suffix.lower() == ".pdf":
            text = read_pdf_file(path)
        else:
            continue
        if text.strip():
            docs.append((path.name, text))
    return docs
