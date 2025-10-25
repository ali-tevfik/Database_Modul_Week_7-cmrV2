from fastapi import FastAPI, APIRouter, HTTPException
from config.config import interviewsSheet
import viewmodels.Interviews_vm as interviews_vm
app = FastAPI()

router = APIRouter(prefix="/interviews")

@router.get("/")
async def get_all_interviews():
    return interviews_vm.get()


@router.get("/project_progress_date")
async def get_project_progress_date():
    return interviews_vm.get_project_progress_date()

@router.get("/project_submission_date")
async def get_project_submission_date():
    return interviews_vm.get_project_submission_date()