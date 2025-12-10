from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String)
    full_name = Column(String)
    contact = Column(String)
    created_at = Column(String)

DATABASE_URL = "postgresql://b_user:b_pass@db-b:5432/b_db"

def create_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine
