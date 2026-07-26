import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "AIM"
VERSION = "1.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-pro"