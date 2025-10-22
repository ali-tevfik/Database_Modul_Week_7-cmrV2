from fastapi import FastAPI, APIRouter, Depends
from db.db import get_db
import viewmodels.CheckFile_vm as checkFile_vm
from sqlalchemy.orm import Session
app = FastAPI()

router = APIRouter(prefix="/checkFile")


@router.get("/")
async def get_all_interviews( db: Session = Depends(get_db)):
    return  await checkFile_vm.get( db)
