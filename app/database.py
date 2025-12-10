from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

#Движок для орм (SQLAlchemy) 

engine = create_engine(
    
    settings.DATABASE_URL,
    echo = True, # логирование запросов (для вывода в консоль))
    pool_pre_ping = True # проверка коннекта с бд
)

#Session maker
SessionLocal = sessionmaker(
    
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base() # род. класс для всех таблиц и моделей в орм