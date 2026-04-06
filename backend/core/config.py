import os
from dotenv import load_dotenv

# Load project root .env first, then load backend/.env to allow backend overrides
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
backend_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(root_env)
load_dotenv(backend_env, override=True)

# Expose keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = os.getenv("TOGETHER_MODEL")
TOGETHER_API_URL = os.getenv("TOGETHER_API_URL", "https://api.together.ai")