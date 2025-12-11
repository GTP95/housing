import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# User information
USER_EMAIL = os.getenv('USER_EMAIL', '')
USER_PASSWORD = os.getenv('USER_PASSWORD', '')
USER_PHONE = os.getenv('USER_PHONE', '')
USER_FIRST_NAME = os.getenv('USER_FIRST_NAME', '')
USER_MIDDLE_NAME = os.getenv('USER_MIDDLE_NAME', '')
USER_LAST_NAME = os.getenv('USER_LAST_NAME', '')
USER_ADDRESS_STREET = os.getenv('USER_ADDRESS_STREET', '')
USER_ADDRESS_NUMBER = os.getenv('USER_ADDRESS_NUMBER', '')
USER_ADDRESS_CITY = os.getenv('USER_ADDRESS_CITY', '')

# Computed full name
USER_FULL_NAME = f"{USER_FIRST_NAME} {USER_LAST_NAME}".strip()
if USER_MIDDLE_NAME:
    USER_FULL_NAME = f"{USER_FIRST_NAME} {USER_MIDDLE_NAME} {USER_LAST_NAME}".strip()
