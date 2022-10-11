import os
from sqlalchemy import (
    create_engine,
    Column,
    BigInteger,
    Boolean,
    String,
    Float,
)
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker


load_dotenv()

host = os.getenv("HOST")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

engine = create_engine(f"postgresql://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    name = Column(String)
    admin = Column(Boolean, default=False)

    def __str__(self):
        return f"{self.username}"


class Contest(Base):
    __tablename__ = "contests"

    name = Column(String, primary_key=True)
    photo = Column(String)
    description = Column(String)
    price = Column(Float)
    winner = Column(String, default=None)

    def __str__(self):
        return f"{self.name}"


class UsersInContests(Base):
    __tablename__ = "users_in_contests"

    payment_id = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String)
    contestname = Column(String)

    def __str__(self):
        return f"{self.user_id} - {self.contestname}"


Base.metadata.create_all(bind=engine)
