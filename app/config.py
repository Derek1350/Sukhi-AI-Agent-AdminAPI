from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

# # Get the directory of the current file (config.py)
# # This will be sukhi_admin_backend/app/
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Go one level up to get to the project root (sukhi_admin_backend/)
# # This is where the .env file is located.
# env_path = os.path.join(current_dir, "..", ".env")
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    
    # New S3 settings
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()

