# models.py
# ---------------------------------------------------------
# Defines our two database tables as Python classes.
# Each class attribute becomes a column in the actual Postgres table.
# ---------------------------------------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """
    One row per signed-up user. 'country' is captured at signup and
    is the single source of truth for which currency this user sees.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # primary_key=True: this column uniquely identifies each row
    # index=True: Postgres builds a fast lookup index on this column

    name = Column(String, nullable=False)
    # nullable=False means this field is required — Postgres will
    # reject any insert that leaves it empty

    email = Column(String, unique=True, nullable=False)
    # unique=True: no two users can share the same email

    password_hash = Column(String, nullable=False)
    # NEVER store the plain password — only the salted hash from
    # auth.hash_password(). See auth.py for how this is created/checked.

    country = Column(String, nullable=False)
    # captured once at signup, drives the currency logic

    city = Column(String, nullable=True)
    # optional — nullable=True means it's allowed to be empty

    currency = Column(String, nullable=False, default="USD")
    # computed at signup time and stored, so we don't recompute it
    # on every single request later

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # server_default=func.now(): Postgres itself fills this in with
    # the current timestamp when the row is inserted


class TripPlan(Base):
    """
    One row per trip-planning run. Stores the final itinerary AND
    the full agent reasoning trace, so past runs stay inspectable.
    """
    __tablename__ = "trip_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ForeignKey links this row to a specific row in the users table

    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    budget_cap = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=True)
    currency = Column(String, nullable=False)

    itinerary = Column(JSON, nullable=True)
    # JSON column: Postgres can store a whole nested Python dict here
    # directly, no need to design separate tables for every sub-field

    trace = Column(JSON, nullable=True)
    # the full agentic AI trace, stored as JSON for later inspection

    created_at = Column(DateTime(timezone=True), server_default=func.now())
