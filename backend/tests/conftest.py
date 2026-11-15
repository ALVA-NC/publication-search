import os
import sys
from pathlib import Path

# Make `app` and `scripts` importable regardless of where pytest is invoked from.
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Provide a dummy API key so `app.config.Settings` can be constructed without
# depending on a real .env file. Environment variables take precedence over the
# dotenv file in pydantic-settings.
os.environ.setdefault("OPENALEX_API_KEY", "test-key")
