import os

class Config:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    if not GITHUB_CLIENT_ID:
        raise ValueError("No GITHUB_CLIENT_ID set for application. Please check the enviroment")
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    if not GITHUB_CLIENT_SECRET:
        raise ValueError("No MONGO_DEFAULT_DATABASE set for application. Please check the enviroment")
