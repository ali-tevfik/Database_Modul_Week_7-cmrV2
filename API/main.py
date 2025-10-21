from fastapi import FastAPI
from views.LoginApi import router as user_router
from views.InterviewsApi import router as interviews_router
from views.MentorApi import router as mentor_router
from views.ApplicationsApi import router as applications_router

app = FastAPI()

app.include_router(user_router)
app.include_router(interviews_router)
app.include_router(mentor_router)
app.include_router(applications_router)