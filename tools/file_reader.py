from pathlib import Path
import pdfplumber


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"File not found: {path}"
    if p.suffix.lower() == ".pdf":
        with pdfplumber.open(p) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    return p.read_text()


def list_files(directory: str, extension: str | None = None) -> list[str]:
    d = Path(directory)
    if not d.exists():
        return []
    files = [f for f in d.iterdir() if f.is_file()]
    if extension:
        ext = extension.lstrip(".")
        files = [f for f in files if f.suffix.lower() == f".{ext}"]
    return [str(f) for f in files]
