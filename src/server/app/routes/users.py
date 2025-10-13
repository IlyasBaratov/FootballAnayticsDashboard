from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


#@router.post("/", response_model=UserCreate)
#def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    #return create_user(db, user)


