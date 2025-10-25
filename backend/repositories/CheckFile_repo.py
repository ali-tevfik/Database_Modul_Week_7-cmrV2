from models.user_model import User
from models.TranieesModel import Trainee
from models.ApplicationsModel import Application
from models.MentorsModel import Mentor
from sqlalchemy.orm import Session
from models.ProjectTrackingModel import ProjectTracking
from datetime import datetime
from models.TranieesModel import Trainee
from models.ApplicationsModel import Application
from config.config import *
from models.MentorsModel import Mentor
import time
from db.db import Base, engine
from datetime import datetime, timedelta

vit_headers = [
"zamandamgasi",	
"adisoyadi",	
"mailadresi",	
"telefonnumarasi",	
"postakodu",	
"yasadigieyalet",	
"ekonomikdurum",
"mentorgorusmesi",
"itphegitimkatilmak",	
"ingilizceseviye",	
"hollandacaseviye",	
"suankidurum",	
"dilkursunadevam",	
"baskigoruyor",	
"bootcampbitirdi",	
"onlineitkursu",	
"ittecrube",	
"projedahil",	
"calismakistegi",	
"nedenkatilmakistiyor",	
"Cybersecurity_Powerplatform", 	
"basvurudonemi",			
]



def parse_sheet_time(sheet_str: str) -> datetime:
    # Z → UTC
    if sheet_str.endswith("Z"):
        sheet_str = sheet_str.replace("Z", "+00:00")
    return datetime.fromisoformat(sheet_str)


def clear_outdated_tables(db: Session):
    # Mapping: (Sheet objesi, Model)
    print("Checking for outdated tables...")
    checks = [
        (LoginSheetTime, User),
        (interviewsSheetTime, ProjectTracking),
        (mentorSheetTime, Mentor),
        (applySheetTime, Application),
        (vit1SheetTime, Application),
        (vit2SheetTime, Application),
    ]

    for sheet, model in checks:
        db_time_tuple = db.query(model.updatedTime).first()
        db_time = db_time_tuple[0] if db_time_tuple else None

        if db_time is None or parse_sheet_time(sheet) > db_time:
            print(f"{model.__tablename__} is outdated → clearing table")
            db.query(model).delete()
            db.commit()
        else:
            print(f"{model.__tablename__} is up to date")


async def checkFile(db):
    Base.metadata.create_all(bind=engine)
    print("Checking initial data... " )
    clear_outdated_tables(db)
    if db.query(User).count()== 0:
        print("user starting(drive)")
        get_user(db)
    if db.query(Mentor).count()== 0:
        print("mentor starting drive")
        add_mentors_from_drive(db)
    if db.query(ProjectTracking).count()== 0:
        print("project starting drive")
        add_project_tracking_from_drive(db)
    if db.query(Application).count()== 0:
        print("application starting drive")


async def checkFile(db):
    Base.metadata.create_all(bind=engine)
    if db.query(User).count()== 0:
        get_user(db)
    if db.query(Mentor).count()== 0:
        add_mentors_from_drive(db)
    if db.query(ProjectTracking).count()== 0:
        add_project_tracking_from_drive(db)
    if db.query(Application).count()== 0:
        apply_data = applySheet.get_all_records()
        print("apply starting")
        add_applications_from_drive(db,apply_data)

        time.sleep(2)

        # Vit1 için: vit1Sheet mevcut headers ile çek
        vit1_headers = [h for h in vit_headers if h in vit1Sheet.row_values(1)]
        time.sleep(2)

        vit1_data = vit1Sheet.get_all_records(expected_headers=vit1_headers)
        print("vit1 starting")
        add_applications_from_drive(db,vit1_data)
            # Vit2 için: vit2Sheet mevcut headers ile çek
        vit2_headers = [h for h in vit_headers if h in vit2Sheet.row_values(1)]
        time.sleep(2)

        vit2_data = vit2Sheet.get_all_records(expected_headers=vit2_headers)
        print("vit2 starting")
        add_applications_from_drive(db,vit2_data)


def get_user(db):
    user_data = LoginSheet.get_all_records()
    for u in user_data:
        create_user(db, u)  


    
def create_user(db: Session, data: dict):
    allowed_keys = {"username", "password", "role"}
    user_data = {k: v for k, v in data.items() if k in allowed_keys}

    new_user = User(**user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  
    

    return new_user

def get_user_by_id(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()



def add_trainees_from_drive(db: Session, name, email, phone_number, postal_code, state, application_period):
    if email:
        isAvailable = db.query(Trainee).filter(Trainee.email == email).first()
    else:
        isAvailable = db.query(Trainee).filter(Trainee.full_name == name).first()
    
    if isAvailable:
        print("return :application_period:", application_period )

        return isAvailable
    
    trainee = Trainee(
        full_name=name,
        email=email or f"noemail_{name.replace(' ', '_')}@example.com",
        phone_number=phone_number,
        postal_code=postal_code,
        state=state,
        application_period=application_period
    )
    db.add(trainee)
    db.commit()
    db.refresh(trainee)

    return trainee

def add_applications_from_drive(db: Session,app_data):
    
    for row in app_data:
        trainee = add_trainees_from_drive(db,row.get('adisoyadi'),row.get('mailadresi'),row.get('telefonnumarasi'),row.get('postakodu'),row.get('yasadigieyalet'),row.get('basvurudonemi'))
        if trainee:
            application = Application(
                trainee_id=trainee.trainee_id,
                application_period=row.get('basvurudonemi'),
                timestamp = datetime.strptime(row['zamandamgasi'], "%m.%d.%Y %H:%M:%S"),
                current_status=row.get('suankidurum'),
                wants_IT_training=row.get('itphegitimkatilmak', 'Hayır') == 'Evet',
                economic_status=row.get('ekonomikdurum'),
                mentor_interview=row.get('mentorgorusmesi', 'Hayır') == 'Evet',
                attending_language_course=row.get('dilkursunadevam', 'Hayır') == 'Evet',
                english_level=row.get('ingilizceseviye'),
                dutch_level=row.get('hollandacaseviye'),
                under_pressure=row.get('baskigoruyor', 'Hayır') == 'Evet',
                completed_bootcamp=row.get('bootcampbitirdi', 'Hayır') == 'Evet',
                online_IT_course=row.get('onlineitkursu', 'Hayır') == 'Evet',
                IT_experience=row.get('ittecrube', 'Hayır') == 'Evet',
                includes_project=row.get('projedahil', 'Hayır') == 'Evet',
                wants_to_work=row.get('calismakistegi', 'Hayır') == 'Evet',
                reason_for_participation=row.get('nedenkatilmakistiyor'),
                Cybersecurity_Powerplatform = row.get("Cybersecurity_Powerplatform")
            )
            db.add(application)
            db.commit()
            db.refresh(application)

def add_mentors_from_drive(db: Session):
    mentor_data = mentorSheet.get_all_records()  # Drive’dan veri çekiyoruz
    for row in mentor_data:
        trainee = add_trainees_from_drive(db,row.get('adisoyadi'),row.get('mailadresi'),row.get('telefonnumarasi'),row.get('postakodu'),row.get('yasadigieyalet'),row.get('BasvuruDonemi'))

        if trainee:
            date_str = row.get('mentorgorusmesi')
            try:
                meeting_date = datetime.strptime(date_str, "%d.%m.%Y")
            except ValueError:
                meeting_date = datetime.strptime(date_str, "%m/%d/%Y")

            mentor = Mentor(
                trainee_id=trainee.trainee_id,
                full_name=row['adisoyadi'],
                meeting_date=meeting_date,
                has_knowledge=row.get('has_knowledge', 'Hayır') == 'Evet',
                can_join_VIT_project=row.get('can_join_VIT_project', 'Hayır') == 'Evet',
                opinion=row.get('opinion'),
                workload=row.get('workload'),
                comments=row.get('comments')
            )
            db.add(mentor)
            db.commit()
            db.refresh(mentor)

def add_project_tracking_from_drive(db: Session):
    project_data = interviewsSheet.get_all_records() 
    for row in project_data:
        trainee = add_trainees_from_drive(
            db,
            row.get('adisoyadi'),
            row.get('mailadresi'),
            row.get('telefonnumarasi'),
            row.get('postakodu'),
            row.get('yasadigieyalet'),
            row.get('basvurudonemi')
        )

        submission_date_str = row.get('Proje gonderilis tarihi')
        progress_date_str = row.get('Projenin gelis tarihi')

        project = ProjectTracking(
            trainee_id=trainee.trainee_id,
            project_submission_date=datetime.strptime(submission_date_str, "%m/%d/%Y") if submission_date_str else None,
            project_progress_date=datetime.strptime(progress_date_str, "%m/%d/%Y") if progress_date_str else None
        )

        db.add(project)
        db.commit()
        db.refresh(project)