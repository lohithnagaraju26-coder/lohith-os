import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.4-mini",
)

# Application configuration
APP_NAME = "LOHITH OS"
APP_VERSION = "0.2"


def validate_config():
    """
    Validate the minimum configuration required
    for live AI functionality.
    """

    if not OPENAI_API_KEY:
        return False, "OPENAI_API_KEY is not configured."

    if not OPENAI_MODEL:
        return False, "OPENAI_MODEL is not configured."

    return True, "Configuration is valid."


if __name__ == "__main__":
    print("LOHITH OS — CONFIGURATION")
    print("=" * 40)
    print()

    print(f"App: {APP_NAME}")
    print(f"Version: {APP_VERSION}")
    print(f"Model: {OPENAI_MODEL}")
    print(f"API key configured: {bool(OPENAI_API_KEY)}")

    valid, message = validate_config()

    print()
    print(message)