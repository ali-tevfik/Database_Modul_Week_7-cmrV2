from fastapi import FastAPI,APIRouter
from fastapi import HTTPException

from config.config import mentorSheet

app = FastAPI()

router = APIRouter(prefix="/mentor")

#crud
@router.get("/getAllMentor")
async def getAllMentor():
   pass