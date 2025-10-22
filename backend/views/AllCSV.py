from fastapi import FastAPI
from fastapi import HTTPException
from config.config import *

app = FastAPI()



vit_headers = [
    "Zaman damgası",
    "Adınız Soyadınız",
    "Mail adresiniz",
    "Telefon Numaranız",
    "Posta Kodunuz",
    "Yaşadığınız Eyalet",
    "Ekonomik Durumunuz",
    "Mentor gorusmesi",
    "Yabancı dil Seviyeniz [İngilizce]",
    "Yabancı dil Seviyeniz [Hollandaca]",
    "Şu anki durumunuz",
    "Şu anda bir dil kursuna devam ediyor musunuz?",
    "Belediyenizden çalışma ile ilgili baskı görüyor musunuz?",
    "Başka bir IT kursu (Bootcamp) bitirdiniz mi?",
    "İnternetten herhangi bir IT kursu takip ettiniz mi (Coursera, Udemy gibi)",
    "Daha önce herhangi bir IT iş tecrübeniz var mı?",
    "Şu anda herhangi bir projeye dahil misiniz? (Öğretmenlik projesi veya Leerwerktraject v.s)",
    "IT sektöründe hangi bölüm veya bölümlerde çalışmak istiyorsunuz ,bir den fazla seçenek seçebilirsiniz",
    "Neden VIT projesine katılmak istiyorsunuz?birden fazla seçenek işaretleyebilirsiniz",
    "Aşağıya bu projeye katılmak veya IT sektöründe kariyer yapmak için sizi harekete geçiren motivasyondan bahseder misiniz?",
    "Yakın zamanda başlayacak ITPH Cybersecurity veya Powerplatform Eğitimlerine Katılmak istemisiniz",
    "Basvuru Donemi",
    "Yesil Tık Olan",
]


@app.get("/getInterview")
async def interview():
    interview = interviewsSheet.get_all_records()
    return interview


@app.get("/getApply")
async def apply():
    try:
        apply = applySheet.get_all_records(expected_headers=vit_headers)
        return apply
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error in apply: {str(e)}")



@app.get("/getMentor")
async def mentor():
    mentor = mentorSheet.get_all_records()
    return mentor
 


@app.get("/getVit1")
async def vit1():
    try:
        vit1 = vit1Sheet.get_all_records(expected_headers=vit_headers)
        return vit1
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error in VIT1: {str(e)}")


@app.get("/getVit2")
async def vit2():
    try:
        vit2 = vit2Sheet.get_all_records(expected_headers=vit_headers)
        return vit2
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error in VIT2: {str(e)}")


@app.get("/getUsers")
async def users():
   try:
        users = LoginSheet.get_all_records()
        return  users
   except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {str(e)}", )

@app.get("/getAllCsv")
async def getAllCsv():
    try:
        interview = interviewsSheet.get_all_records()
        apply = applySheet.get_all_records(expected_headers=vit_headers)
        users = LoginSheet.get_all_records()
        vit2 = vit2Sheet.get_all_records(expected_headers=vit_headers)
        vit1 = vit1Sheet.get_all_records(expected_headers=vit_headers)
        mentor = mentorSheet.get_all_records()

        return { 
            "users": users, 
            "interview": interview, 
            "apply": apply, 
            "mentor": mentor, 
            "vit1": vit1, 
            "vit2": vit2
            }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {str(e)}", )
