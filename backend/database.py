# database.py
# ---------------------------------------------------------
# Sets up the connection to PostgreSQL using SQLAlchemy,
# an ORM (Object-Relational Mapper) that lets us work with
# database rows as if they were normal Python objects.
# ---------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# The "engine" manages the actual connection pool to Postgres.
# It doesn't connect immediately — it connects lazily on first use.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory: calling SessionLocal() gives us a new
# "session" — basically an open conversation with the database that
# we can query and commit changes through.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class every database table (model) will inherit
# from. SQLAlchemy uses this to know which Python classes map to tables.
Base = declarative_base()


def get_db():
    """
    A FastAPI 'dependency' — FastAPI calls this automatically for any
    route that asks for a db session, and guarantees the session is
    closed afterward, even if the request raises an error.
    """
    db = SessionLocal()       # open a new session for this one request
    try:
        yield db               # hand it to the route function
    finally:
        db.close()             # always clean up, success or failure
