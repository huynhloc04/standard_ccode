from sqlalchemy import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)

def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield session
    finally:
        sessionmaker.close()
        

def init_db() :
    SQLModel.metadata.create_all(engine)