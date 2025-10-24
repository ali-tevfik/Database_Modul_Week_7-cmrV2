from fastapi import FastAPI, APIRouter, HTTPException
from config.config import applySheet
import viewmodels.applications_vm as applications_vm
app = FastAPI()

router = APIRouter(prefix="/applications")

#crud
@router.get("/")
async def get_applications():
    return applications_vm.get()

#crud
@router.get("/searchName/{searchText}")
async def get_applications(searchText):
    return applications_vm.searchText(searchText)

#
@router.get("/getAll")
async def get_applications():
    return applications_vm.getAll()

@router.get("/showmentor")
async def get_applications():
    return applications_vm.showmentor()

@router.get("/ushowmentor")
async def get_applications():
    return applications_vm.ushowmentor()

@router.get("/dublicate")
async def get_applications():
    return applications_vm.dublicate()

@router.get("/fltered")
async def get_applications():
    return applications_vm.fltered()

@router.get("/prevvitcheck")
async def get_applications():
    return applications_vm.prevvitcheck()

@router.get("/differenreg")
async def get_applications():
    return applications_vm.differenreg()