import os

class Config:
    """Base configuration variables."""
    MONGO_URL = os.getenv('MONGO_URL')
    if not MONGO_URL:
        raise ValueError("No MONGO_URL set for application. Please check the enviroment")
    MONGO_DEFAULT_DATABASE = os.getenv('MONGO_DEFAULT_DATABASE')
    if not MONGO_DEFAULT_DATABASE:
        raise ValueError("No MONGO_DEFAULT_DATABASE set for application. Please check the enviroment")