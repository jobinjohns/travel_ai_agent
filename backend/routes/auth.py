# routes/auth.py
# ---------------------------------------------------------
# Sign up and sign in. These are the only two routes that don't
# require a token — everything else in the app does.
# ---------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from schemas import UserSignup, UserLogin, TokenResponse
from currency import get_currency_for_country
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    """
    Creates a new account and signs the user straight in — the
    response includes a ready-to-use token, so the frontend doesn't
    need a separate login call right after signing up.
    """
    currency = get_currency_for_country(data.country)

    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        country=data.country,
        city=data.city,
        currency=currency,
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists. Please sign in instead.",
        )
    db.refresh(new_user)

    token = create_access_token(new_user.id)
    return TokenResponse(access_token=token, user=new_user)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Verifies email + password and returns a fresh session token."""
    user = db.query(User).filter(User.email == data.email).first()

    # Deliberately the SAME error message whether the email doesn't
    # exist or the password is wrong — telling them apart would let an
    # attacker discover which emails have accounts on this site
    incorrect = HTTPException(status_code=401, detail="Incorrect email or password.")

    if not user:
        raise incorrect
    if not verify_password(data.password, user.password_hash):
        raise incorrect

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=user)
