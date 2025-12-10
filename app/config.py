# pydantic настройки  

from pydantic_settings import BaseSettings # для типизации

class Settings(BaseSettings):

    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True #для регистра

settings = Settings() #экземпляр 
