from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

#Движок для орм (SQLAlchemy) 

engine = create_engine(
    
    settings.DATABASE_URL,
    echo = True, # логирование запросов 
    pool_pre_ping = True 
)

#Session maker
SessionLocal = sessionmaker(
    
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base() 