import os

class Config:
    """Base configuration variables."""
    MONGO_HOST = os.getenv('MONGO_HOST')
    if not MONGO_HOST:
        raise ValueError("No MONGO_HOST set for application. Please check the enviroment")
    MONGO_USER_NAME = os.getenv('MONGO_USER_NAME')
    if not MONGO_USER_NAME:
        raise ValueError("No MONGO_USER_NAME set for application. Please check the enviroment")
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    if not MONGO_PASSWORD:
        raise ValueError("No MONGO_PASSWORD set for application. Please check the enviroment")
    MONGO_DEFAULT_DATABASE = os.getenv('MONGO_DEFAULT_DATABASE')
    if not MONGO_DEFAULT_DATABASE:
        raise ValueError("No MONGO_DEFAULT_DATABASE set for application. Please check the enviroment")

