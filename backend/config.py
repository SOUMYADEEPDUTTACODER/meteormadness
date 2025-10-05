import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/neo/rest/v1/neo"