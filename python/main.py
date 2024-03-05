import random,os,smtplib,string,shutil
from dotenv import load_dotenv
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request,Form,UploadFile,File
from jose import JWTError,jwt
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import List
# from consumer import consume_from_kafka
# from client import producer
# print("---------------------------------------------------**********************************")
# # print(SECRET)
load_dotenv()
SECRET= os.getenv("secret_key")
ALGORITHM=os.getenv("algorithms")
senderemail=os.getenv("senderemail")
passkey=os.getenv("passkey")
host=os.getenv("host")
port=os.getenv("port")
app=FastAPI()
global otemail
# sessions={}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


client=MongoClient(os.getenv("connectdb"))
app.add_middleware(SessionMiddleware, secret_key = SECRET )
errors={}
# connecting database
dblist=client.list_database_names()
if "logdata" in dblist:
    db=client["logdata"]
    collist=db.list_collection_names()
    if "users" in collist:
        col=db["users"]
else:
    db=client["logdata"]
    col=db["users"]

# directing to directories
template=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

# the below code load a landing web page
@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return template.TemplateResponse("landing.html",{"request":request})
    # errors["signup"]=" "
    # return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":None})

# the below code load a signup web page
@app.get("/signup",response_class=HTMLResponse)
async def signuppage(request:Request):
    errors["signup"]=" "
    return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":None})

# the below code get data from signup page and verify data before inserting to database
@app.post("/signuptodb") #--
async def signuptodb(request:Request,username:str = Form() ,email:str=Form(), password:str=Form(),con_password:str=Form(),Captcha:str=Form(),incap:str=Form()):
    hashed_password = pwd_context.hash(password)
    is_correct = pwd_context.verify(con_password, hashed_password)
    userdata={
        "username":username,
        "email":email,
        "password":hashed_password,
        "profile":"static/images/user.png",
        "status":"active"
    }
    ckcap=incap
    d={
        "user":username,
        "email":email,
        "pwd":password
    }
    alreadyin=col.find_one({"username":username})
    if alreadyin==None:
        alemail=col.find_one({"email":email})
        if alemail==None:
            if is_correct:
                if Captcha==ckcap:
                    col.insert_one(userdata)
                    request.session['user'] = username
                    return RedirectResponse(url=f"/dashboard", status_code=307)
                    # return signin_fun(username,request)
                else:
                    errors['signup']="cap"
                    return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":d})
            else:
                errors['signup']="pwd"
                return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":d})
        else:
            errors['signup']="email"
            return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":d})
    else:
        errors['signup']="user"
        return template.TemplateResponse("signup.html",{"request":request,"error":errors,"dat":d})
    
# the below code load a signin web page when signin endpoint get in url 
@app.get("/signin",response_class=HTMLResponse)
async def signinpage(request:Request):
    errors['signin']=" "
    return template.TemplateResponse("signin.html",{"request":request,"error":errors})

# the below code load a signintodb web page when signintodb endpoint get in url 
# the below code verify the user in database or not if user found and with correct password 
# then it return to website with session id
@app.post("/signintodb")
def signintodb(request:Request,username:str=Form(),password:str=Form()):
    user={"username":username}
    dbuser=col.find_one(user)
    if dbuser==None:
        errors['signin']="user"
        return template.TemplateResponse("signin.html",{"request":request,"error":errors})
    else:
        is_correct = pwd_context.verify(password, dbuser["password"])
        if is_correct:
            col.update_one({"username":username},{"$set":{"status":"active"}})
            return signin_fun(username,request)
        else:
            errors['signin']="pwd"
            return template.TemplateResponse("signin.html",{"request":request,"error":errors,"user":username})


# the below code load the forgetpwd.html  when forgetpwd endpoint get in url 
@app.get("/forgetpwd")
async def signinpage(request:Request):
    errors['changepwd']=" "
    return template.TemplateResponse("forgetpwd.html",{"request":request,"error":errors})

# the below code load a updatepwdcon when updatepwdcon endpoint get in url ***
@app.post("/updatepwdcon") # $
async def updatepwdcon(request:Request,username:str=Form(),old_password:str=Form(),new_password:str=Form(),con_password:str=Form()):
    user={"username":username}
    new_hashed_password = pwd_context.hash(new_password)
    o_user={"username":username}
    n_user={"$set":{"username":username,"password":new_hashed_password}}
    dbuser=col.find_one(user)

    is_correct = pwd_context.verify(old_password, dbuser["password"])
    if is_correct:
        if old_password==new_password:
            # return{"msg":"same"}
            errors['changepwd']="same"
            return template.TemplateResponse("forgetpwd.html",{"request":request,"error":errors})

        else:
            if new_password==con_password:
                col.update_one(o_user,n_user)
                return signin_fun(username,request)
            else:
                errors['changepwd']="newcon"
                return template.TemplateResponse("forgetpwd.html",{"request":request,"error":errors})

                # return{"msg":"newcon"}
    errors['changepwd']="incor"
    return template.TemplateResponse("forgetpwd.html",{"request":request,"error":errors})

    # return{"msg":"incor"}


# the below code load a otp.html web page when passwordotp endpoint get in url 
@app.get("/passwordotp",response_class=HTMLResponse)
async def passwordotp(request:Request):
    errors['otp']=" "
    return template.TemplateResponse("otp.html",{"request":request,"email":" ","error":errors})

@app.post("/otp",response_class=HTMLResponse)
async def forgot_password(request: Request,email: str= Form()):
    user = col.find_one({"email": email})
    # global otemail
    otemail=email
    if not user:
        errors['otp']="nouser"
        return template.TemplateResponse("otp.html",{"request":request,"email":otemail,"error":errors})
        # raise HTTPException(status_code=400, detail="User not found")
    
    otp = ''.join(random.choices(string.digits, k=6))
    user["otp"] = otp
    col.update_one({"_id": ObjectId(user["_id"])}, {"$set": user})
    # below block helps to send to user email of otp as email 
    server = smtplib.SMTP(host,port)
    server.starttls()
    server.login(senderemail,passkey)
    message = 'Subject: {}\n\n{}'.format('OTP for password reset', 'Your OTP is: ' + otp)
    server.sendmail(senderemail, user["email"], message)
    server.quit()
    errors['otp']="success"
    return template.TemplateResponse("otp.html",{"request":request,"email":otemail,"error":errors})
        
# ***
@app.post("/checkotp")
async def checkotp(request:Request,emaill:str=Form(),otp:str=Form(),newpwd:str=Form(),conpwd:str=Form()):
    olddata={"email":emaill}
    ckotp = col.find_one(olddata)
    if ckotp["otp"]==otp:
        if newpwd==conpwd:
            new_hashed_password = pwd_context.hash(newpwd)
            newdata={ "$set": {"email":emaill,"password":new_hashed_password}}
            updata=col.update_one(olddata,newdata)
            usr=col.find_one({"email":emaill})
            request.session['user'] = usr["username"]
            # return RedirectResponse(url=f"/dashboard", status_code=307)
            errors['otp']="success2"
            return template.TemplateResponse("otp.html",{"request":request,"email":emaill,"error":errors})

            # return signin_fun(username,request)
        else:
            errors['otp']="pwd"
            return template.TemplateResponse("otp.html",{"request":request,"email":emaill,"error":errors})
    else:
        errors['otp']="otp"
        return template.TemplateResponse("otp.html",{"request":request,"email":emaill,"error":errors})

@app.post("/decode")
async def decode(request:Request,getted_token:dict):
    checked=check_token(getted_token["toke"])
    user=checked["username"]
    data=col.find_one({"username":user},{"_id":0})
    try:
        request.session['user'] = data['username']
        # request.session.save()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/logout")   
async def logout(request:Request): 
    user = request.session.get('user')
    col.update_one({"username":user},{"$set":{"status":"inactive"}})
    return template.TemplateResponse("landing.html",{"request":request})

    # errors['signin']=" "
    # return template.TemplateResponse("signin.html",{"request":request,"error":errors})

@app.get("/logstatus")
async def logstat(request:Request):
    logstat=request.session.get("logstat", None)
    stat=jsonable_encoder(logstat)
    return stat

@app.post("/imatodb")
async def imatodb(request: Request, profile: UploadFile = File(), user: str = Form()):
    if profile.filename:
        filenae=user+profile.filename
        already=os.path.join("static/images/",profile.filename )
        path = os.path.join("static/images/",filenae )
        udata=col.find_one({"username":user})
        if already==udata['profile'] or path==udata['profile']:
            a=a
        else:
            with open(path, "wb") as f:
                shutil.copyfileobj(profile.file, f)
            col.update_one({"username": user}, {"$set": {"profile": path}})
        request.session['user'] = user
        return RedirectResponse(url=f"/dashboard", status_code=307)
@app.get("/dashboard")
def backlogin(request: Request):
    user = request.session.get('user')
    if not user:
        return {"message": "User parameter not found in query params"}
    return signin_fun(user, request)

@app.post("/dashboard")
async def dashboard(request:Request):
    user = request.session.get('user')
    if not user:
        return {"message": "User parameter not found in query params"}
    return signin_fun(user, request)

@app.post("/delpro")
async def process_data(user: dict):
    user_data = col.find_one({"username": user['user']}, {"_id": 0})
    path=user_data['profile']
    if user_data["profile"] == "static/images/user.png":
        print("this oneeee")
        return None
    else:
        if os.path.exists(user_data['profile']):
            os.remove(user_data['profile'])
        col.update_one(
            {"username": user['user']},
            {"$set": {"profile" : "static/images/user.png"}}
        )
        return user_data

@app.post("/shipdetails")
async def shipdetails(request   :Request,
                      emailship :str=Form(),
                      ship_no   :str=Form(),
                      route     :str=Form(),
                      device    :str=Form(),
                      po_no     :str=Form(),
                      ndc_no    :str=Form(),
                      serial_no :str=Form(),
                      con_no    :str=Form(),
                      good_type :str=Form(),
                      ex_date   :str=Form(),
                      del_no    :str=Form(),
                      batch_id  :str=Form(),
                      desc      :str=Form()
                      ):
    data={
        "email"         :emailship,
        "ship_no"       :ship_no,
        "route"         :route,
        "device"        :device,
        "po_no"         :po_no,
        "ndc_no"        :ndc_no,
        "serial_no"     :serial_no,
        "con_no"        :con_no,
        "goods_type"    :good_type,
        "ex_date"       :ex_date,
        "del_no"        :del_no,
        "batch_id"      :batch_id,
        "desc"          :desc,
        }
    
    user = request.session.get('user')
    userd="shipment_data"
    usercol=db[userd]
    d=usercol.find_one({"ship_no":ship_no},{"_id":0})
    if d:
        return{"msg":"check shipmentid"}
    else:
        usercol.insert_one(data)
        return signin_fun(user,request)
    
# ########################################################################################################################
# methods#
    
def signin_fun(username,request,dis=None):
    status=col.find_one({"username":username})
    data={}
    if status["status"]=="inactive":
        errors['signin']=" "
        return template.TemplateResponse("signin.html",{"request":request,"error":errors})
    else:
        if username is not None:
            token=create_token(username)
            u="shipment_data"
            usercol=db[u]
            redata=usercol.find({"email":status["email"]})
            Isadmin=False
            if username=="ADMIN":
                decol=db['devicedata']
                dev_data=decol.find({},{"_id":0})
                k=0
                for i in dev_data:
                    k+=1
                    data[k]=i
                Isadmin=True
            if token:
                return template.TemplateResponse("dashboard.html",{"request":request,"token":token,"dis":redata,"Isadmin":Isadmin,"devdata":data})
    
def create_token(username):
    user_payload = {"username": username}
    entoken = jwt.encode(user_payload, SECRET, ALGORITHM)
    if entoken:
        return entoken
    
# capgen method generates and return captcha also assigning to capg global variable
def capgen(a=0):
    global capg
    if a==1:
        captcha =''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        capg=captcha
        return captcha
    return capg

# gen_ran_id always genarates and return a random id
def gen_ran_id():
    rand_id = len("helllo") + random.randint(0, 1000000)
    return rand_id

# gen_unique_id get random id from gen_ran_id method and checks wether random id is in sessions(dictionary)
#  if no such id found in sessions it returns that id
def gen_unique_id(dictionary):
    while True:
        unique_id = gen_ran_id()
        if unique_id not in dictionary:
            return unique_id
          
def check_token(g_token):
    received_token =g_token
    try:
        decoded_token = jwt.decode(received_token, SECRET , ALGORITHM)
        return decoded_token
        print("Decoded Token:", decoded_token)
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token. Authentication failed.")
    