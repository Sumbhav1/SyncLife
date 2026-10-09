import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    JWT_SECRET = os.getenv("JWT_SECRET")
    SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")
    # Any local port by default, since Vite moves to 5174+ when 5173 is taken
    CORS_ORIGINS = (os.getenv("CORS_ORIGINS").split(",") if os.getenv("CORS_ORIGINS")
                    else [r"http://localhost:\d+", r"http://127\.0\.0\.1:\d+"])
