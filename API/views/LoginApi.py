from fastapi import FastAPI, APIRouter, Depends
from models.LoginModel import LoginModel
from config.config import LoginSheet
from sqlalchemy.orm import Session
from db import get_db
from viewmodels import user_vm
from db import get_db, Base, engine
app = FastAPI()
router = APIRouter(prefix="/user") 

Base.metadata.create_all(bind=engine)

@router.post("/login")
async def login(data: LoginModel, db: Session = Depends(get_db)):
    return await user_vm.login_vm(db, data.username, data.password)


@router.get("/getalluser")
def getuser():
    record = LoginSheet.get_all_records()
    return record

app.include_router(router)
