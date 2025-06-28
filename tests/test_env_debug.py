# test_env_debug.py
from dotenv import load_dotenv
import os

success = load_dotenv(override=True)
print("✅ .env loaded:", success)
print("🔍 BACKEND_URL =", os.getenv("BACKEND_URL"))
