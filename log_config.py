import os

class LogConfig:
    LOG_LEVEL = os.getenv('LOG_LEVEL')
    if not LOG_LEVEL:
        raise ValueError("No LOG_LEVEL set for application. Please check the enviroment")
    # Adding the loggly token is optional so don't raise an exception if not present
    LOGGLY_TOKEN = os.getenv('LOGGLY_TOKEN')
