from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

MODEL = "Qwen/Qwen2.5-7B-Instruct"

def ask_ai(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are AIM, a smart AI assistant similar to Jarvis. "
                    "Be concise, friendly, and helpful."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content