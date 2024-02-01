import smtplib
from fastapi import FastAPI, Form,Request,Response
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext


client=MongoClient("mongodb+srv://Yadav5111:Yadav5111@foster.4kutoov.mongodb.net/")

app=FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dblist=client.list_database_names()
if "logdata" in dblist:
    db=client["logdata"]
    collist=db.list_collection_names()
    if "users" in collist:
        col=db["admin"]
else:
    db=client["logdata"]
    col=db["admin"]


template=Jinja2Templates(directory="../admin/admin_templates")
app.mount("/static",StaticFiles(directory="../admin/admin_static"),name="static")

@app.get("/")
async def adminlogin(request:Request):
    return template.TemplateResponse("adminlogin.html",{"request":request})

# global alert
# alert=0
@app.post("/admin_login")
async def admin_login(request:Request,admin:str=Form(),password:str=Form()):
    hashed_password = pwd_context.hash(password)
    adminpassword=col.find_one({"admin":"Admin"})
    alert=adminpassword['alert']
    is_correct = pwd_context.verify(adminpassword["pwd"], hashed_password)
    if is_correct:
        col.update_one({"admin":"Admin"},{"$set":{"alert":0}})
        return template.TemplateResponse("dashboard.html",{"request":request})
    else:
        alert+=1
        col.update_one({"admin":"Admin"},{"$set":{"alert":alert}})
        if alert<3:
            return template.TemplateResponse("adminlogin.html",{"request":request})
        else:
            return{"msg":"You have tried more than "+alert-1}
        

# @app.get("/admin_login/dashboard")
# async def dashboard(request:Request):

#     # return template.TemplateResponse("dashboard.html",{"request":request})
        





