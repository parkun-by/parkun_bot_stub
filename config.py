from os import getenv
from os.path import join, dirname
from aiohttp.client import DEFAULT_TIMEOUT
from dotenv import load_dotenv

SEPARATOR = ";:"

# Create .env file path.
dotenv_path = join(dirname(__file__), ".env")

# Load file from the path.
load_dotenv(dotenv_path)

BOT_TOKEN = getenv('BOT_TOKEN', "")
WELCOME_TEXT = getenv('WELCOME_TEXT', "").replace(SEPARATOR, "\n")
CAT_URL = getenv('CAT_URL', "https://api.thecatapi.com/v1/images/search")
