from openai import OpenAI


import json
import numpy as np
from openai import OpenAI

from src.config import settings
from src.embedder import embed_texts, cosine_similarity

api_key=settings.openai_api_key
client = OpenAI(api_key=api_key)
try:

    models = client.models.list()
    print("SUCCESS", len(models.data))
except Exception as e:
    import traceback
    print("ERROR TYPE:", type(e))
    print("ERROR REPR:", repr(e))
    traceback.print_exc()
