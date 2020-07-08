import os

class Config:
    """Base configuration variables."""
    TRELLO_BASE_URL = os.getenv('TRELLO_BASE_URL')
    if not TRELLO_BASE_URL:
        raise ValueError("No TRELLO_BASE_URL set for application. Please check .env")
    TRELLO_KEY = os.getenv('TRELLO_KEY')
    if not TRELLO_KEY:
        raise ValueError("No TRELLO_KEY set for application. Please check .env")
    TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
    if not TRELLO_TOKEN:
        raise ValueError("No TRELLO_TOKEN set for application. Please check .env")

