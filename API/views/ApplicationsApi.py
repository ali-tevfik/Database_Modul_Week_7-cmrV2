from fastapi import FastAPI,APIRouter


app = FastAPI()

router = APIRouter(prefix="/applications")

#crud
@router.get("/")
async def getAllMentor():
  return "Fahri bey"

