from fastapi import FastAPI,APIRouter
from fastapi import HTTPException
import viewmodels.mentor_vm as mentor_vm

from config.config import mentorSheet

app = FastAPI()

router = APIRouter(prefix="/mentor")

#crud
@router.get("/")
async def getAllMentor():
   return mentor_vm.mentor_vm()
   
@router.get("/findName/{searchtText}")
async def getMentorByName(searchtText:str):
   return mentor_vm.findMentorByName_vm(searchtText)


@router.get("/comboBoxValuesFilter/{filter}")
async def getComboBoxValuesFilter(filter:str):
   print("MentorApi getComboBoxValuesFilter called with filter:", filter)
   return mentor_vm.findMentorByComboBox_vm(filter)