import os

class Config:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    if not GITHUB_CLIENT_ID:
        raise ValueError("No GITHUB_CLIENT_ID set for application. Please check the enviroment")
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    if not GITHUB_CLIENT_SECRET:
        raise ValueError("No GITHUB_CLIENT_SECRET set for application. Please check the enviroment")
    GITHUB_LOGON_REDIRECT = os.getenv('GITHUB_LOGON_REDIRECT')
    if not GITHUB_LOGON_REDIRECT:
        raise ValueError("No GITHUB_LOGON_REDIRECT set for application. Please check the enviroment")
