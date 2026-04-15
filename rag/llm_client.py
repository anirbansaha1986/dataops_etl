import requests
from utils.logger import get_logger

logger = get_logger("LLM")

API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "google/gemma-3-4b"


def ask_llm(prompt):

    logger.info("Calling Gemma LLM")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(API_URL, json=payload)

    return response.json()["choices"][0]["message"]["content"]