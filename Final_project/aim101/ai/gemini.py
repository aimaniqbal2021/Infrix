from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
# print("HF_TOKEN:", HF_TOKEN) for testing api work
client = None

if HF_TOKEN:
    client = InferenceClient(api_key=HF_TOKEN)

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"


def ask_gemini(prompt: str):
    if client is None:
        return (
            "⚠ Hugging Face token not configured.\n\n"
            "Create a .env file and add:\n"
            "HF_TOKEN=YOUR_TOKEN"
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are AIM, a Jarvis-like AI assistant. "
                        "Answer clearly, briefly, and helpfully."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"







# from google import genai
# from config import GEMINI_API_KEY, MODEL_NAME

# client = None

# if GEMINI_API_KEY:
#     client = genai.Client(api_key=GEMINI_API_KEY)


# def ask_gemini(prompt: str):
#     if client is None:
#         return (
#             "⚠ Gemini API key not configured.\n\n"
#             "Create a .env file and add:\n"
#             "GEMINI_API_KEY=YOUR_API_KEY"
#         )

#     try:
#         response = client.models.generate_content(
#             model=MODEL_NAME,
#             contents=prompt,
#         )

#         return response.text

#     except Exception as e:
#         return f"Error: {e}"