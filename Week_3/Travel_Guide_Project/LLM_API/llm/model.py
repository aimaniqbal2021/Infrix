import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"


def generate_text(messages, token, model="Qwen/Qwen2.5-7B-Instruct", max_tokens=300):
    """
    messages: list of {"role": "system"|"user"|"assistant", "content": str}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise ValueError(f"HF API error {response.status_code}: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
