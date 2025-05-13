import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), r'..\..')))

from dotenv import load_dotenv

# Load environment variables from .env file in the backend directory
# Assumes .env is in backend/ and conftest.py is in backend/tests/
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)