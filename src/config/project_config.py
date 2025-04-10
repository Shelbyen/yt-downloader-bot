from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    VERSION: str
    DOWNLOADER: str
    ADMINS: str
