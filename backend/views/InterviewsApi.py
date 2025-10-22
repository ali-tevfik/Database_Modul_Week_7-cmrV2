from fastapi import FastAPI, APIRouter, HTTPException
from config.config import interviewsSheet
import viewmodels.Interviews_vm as interviews_vm
app = FastAPI()

router = APIRouter(prefix="/interviews")

@router.get("/")
async def get_all_interviews():
    return interviews_vm.get()
    # try:
    #     records = interviewsSheet.get_all_records()
    #     return records
    # except:
    #     raise HTTPException(status_code=401, detail="Error ")
