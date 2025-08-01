#database.py-Valencia Walkers
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/openq")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
