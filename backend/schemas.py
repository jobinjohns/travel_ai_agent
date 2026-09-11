# schemas.py
# ---------------------------------------------------------
# Pydantic models describe the *shape* of data going in/out of the
# API, and validate it automatically at the door — e.g. rejecting a
# short password or a negative budget before it ever reaches an agent.
# ---------------------------------------------------------
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSignup(BaseModel):
    """What the frontend sends to create a new account."""
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)
    country: str = Field(min_length=1)
    city: Optional[str] = None


class UserLogin(BaseModel):
    """What the frontend sends to sign in."""
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """The user info we're comfortable sending back to the frontend.
    Notice there's no password or password_hash field here — it's
    simply never included in any response."""
    id: int
    name: str
    email: str
    country: str
    currency: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """What both /auth/signup and /auth/login return: a session token
    plus the user's own info, in one response."""
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TripRequest(BaseModel):
    """
    What the frontend sends to plan a trip. Notice there's no user_id
    here anymore — which user is asking comes from their JWT token
    (see auth.get_current_user_id), never from a field the client
    could simply edit to plan a trip "as" someone else.
    """
    origin: str = Field(min_length=1)
    destination: str = Field(min_length=1)
    start_date: str
    end_date: str
    budget_cap: float = Field(gt=0)
