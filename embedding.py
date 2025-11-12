import os
from typing import List, Sequence, Dict
from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

_NEW_SDK = True
try:
    from openai import OpenAI
    _client = OpenAI()
except Exception:
    _NEW_SDK = False
    import openai


def get_embedding(text: str) -> List[float]:
    text = text.replace("\n", " ")
    if _NEW_SDK:
        r = _client.embeddings.create(model=EMBED_MODEL, input=text)
        return r.data[0].embedding
    else:
        r = openai.Embedding.create(model=EMBED_MODEL, input=text)
        return r["data"][0]["embedding"]


def chat_complete_text(messages: Sequence[Dict[str, str]]) -> str:
    models = [CHAT_MODEL, "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    last_err = None
    for m in models:
        try:
            if _NEW_SDK:
                resp = _client.chat.completions.create(model=m, messages=messages)
                return resp.choices[0].message.content
            else:
                resp = openai.ChatCompletion.create(model=m, messages=messages)
                return resp["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"OpenAI chat failed. Last error: {repr(last_err)}")
