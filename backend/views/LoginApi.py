from fastapi import FastAPI, APIRouter, Depends
from models.LoginModel import LoginModel
from config.config import LoginSheet
from sqlalchemy.orm import Session
from db.db import get_db, Base, engine
from viewmodels import user_vm
import time


app = FastAPI()
router = APIRouter(prefix="/user") 

Base.metadata.create_all(bind=engine)

@router.post("/login")
async def login(data: LoginModel, db: Session = Depends(get_db)):
    return await user_vm.login_vm(db, data.username, data.password)






app.include_router(router)
