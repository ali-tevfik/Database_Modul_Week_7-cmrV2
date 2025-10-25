import gspread
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
cred_file = os.path.join(BASE_DIR, "vit8-credentials.json")
client = gspread.service_account(filename=cred_file)
LoginSheet = client.open("Kullanicilar").get_worksheet(0)
interviewsSheet = client.open("Mulakatlar").get_worksheet(0)
mentorSheet = client.open("Mentor").get_worksheet(0)
applySheet = client.open("Applications").get_worksheet(0)
vit1Sheet = client.open("VIT1").get_worksheet(0)
vit2Sheet = client.open("VIT2").get_worksheet(0)


LoginSheetTime = client.open("Kullanicilar").get_lastUpdateTime()
interviewsSheetTime = client.open("Mulakatlar").get_lastUpdateTime()
mentorSheetTime = client.open("Mentor").get_lastUpdateTime()
applySheetTime = client.open("Applications").get_lastUpdateTime()
vit1SheetTime = client.open("VIT1").get_lastUpdateTime()
vit2SheetTime = client.open("VIT2").get_lastUpdateTime()

