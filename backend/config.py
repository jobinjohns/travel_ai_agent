# config.py
# ---------------------------------------------------------
# Loads environment variables from the .env file into Python, so
# every other file can just import from here instead of calling
# os.getenv() everywhere.
# ---------------------------------------------------------
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Used to sign/verify JWT login tokens. This MUST be a long random
# secret in any real deployment — anyone who has it can forge valid
# tokens for any user. The .env.example includes a placeholder;
# generate a real one with: python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-insecure-secret-change-me")
