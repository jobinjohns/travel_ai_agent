# routes/users.py
# ---------------------------------------------------------
# Everything here requires a valid token — there's no more "fetch any
# user by ID" route, since that let anyone look up anyone else's
# profile just by guessing a number.
# ---------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserOut
from auth import get_current_user_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_my_profile(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Returns the signed-in user's own profile, identified from their token."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
