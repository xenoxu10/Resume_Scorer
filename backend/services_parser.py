import fitz  # PyMuPDF
from docx import Document
from typing import Union
import io


async def parse_file(file_content: bytes, filename: str) -> str:
    """
    Parse PDF or DOCX files and extract text
    
    Args:
        file_content: File bytes
        filename: Original filename to determine file type
    
    Returns:
        Extracted text content
    """
    try:
        if filename.endswith(".pdf"):
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        
        elif filename.endswith(".docx"):
            doc = Document(io.BytesIO(file_content))
            text = "\n".join([p.text for p in doc.paragraphs])
            return text.strip()
        
        elif filename.endswith(".txt"):
            return file_content.decode("utf-8").strip()
        
        else:
            return file_content.decode("utf-8").strip()
    
    except Exception as e:
        raise ValueError(f"Error parsing file {filename}: {str(e)}")
