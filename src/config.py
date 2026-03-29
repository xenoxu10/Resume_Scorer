import os
from dataclasses import dataclass

from dotenv import load_dotenv


# Load variables from a .env file in the project root (if present)
load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    resumes_dir: str = os.getenv("RESUMES_DIR", "Resume")
    jds_dir: str = os.getenv("JDS_DIR", "JD")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4.1-mini")


settings = Settings()
