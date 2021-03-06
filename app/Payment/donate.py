from fastapi import Depends,File, UploadFile, APIRouter,Request
from fastapi.templating import Jinja2Templates
import uuid, datetime
from app.talent.database import SessionLocal, engine, database
from starlette.responses import RedirectResponse
import razorpay
from fastapi.responses import HTMLResponse
from app.authentication import schemas, models
from app.authentication.models import Course
#from . import models,schemas
router = APIRouter()

templates = Jinja2Templates(directory="templates")

# @router.get("/payment/")
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
from random import randint
# @router.post("/payment/")
# async def home_pay(pay : schemas.PaidBase, request: Request):
#     #id=None
#     gid = randint(100000,1000000)
#     gdate = datetime.datetime.now()
#     print(router)
#     query = models.Paid.__table__.insert().values(
#         id = gid,
#         name = pay.name,
#         #email = pay.email,
#         amount= pay.amount,
#         created_date = gdate)
#     print("hello")
#     await database.execute(query)
#     print("executed")
#     #id=pay.id
#     #url = router.url_path_for("pay",id=models.Paid.id)
#     # url = request.url_for("pay"   ,id=models.Paid.id)
#     # print(url)
#     # response = RedirectResponse(url=url)#id=models.Payment.id
#     # print("fine")
#     # return response
#     return {
#         **pay.dict(),
#         "id" :gid,
#         "created_at" : gdate,
#     }
    #return templates.TemplateResponse("index.html", {"request": request})
import pandas as pd
# 

@router.get("/pay/{id}",response_class=HTMLResponse)
async def pay_me(request: Request, id:str):
    #pay = models.Payment.__table__.select(models.Payment.amount).where(models.Payment.id==id)
    
    pay =  "SELECT courses.price FROM courses WHERE courses.id ="+str(id)
    #pay1 =  "SELECT courses.name FROM courses WHERE courses.id ="+str(id)
    pay1 = Course.__table__.select(models.Course.name).where(models.Course.id==id)
    result = await database.execute(pay)
    database.execute(pay1)
    print(pay)
    gid = randint(100000,1000000)
    gdate = datetime.datetime.now()
    
    # any = models.Payment.amount
    #print(result)
    print(pay1)
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w","dcPlBgM8Fv7H2J1cYISFKC81"))
    payment = client.order.create({'amount' : int(df.price.values)*100, 'currency':'INR', 'receipt': 'TEST','payment_capture':'1'})
    
    return templates.TemplateResponse("pay.html", {"request": request, "payment":payment})

@router.get("/success/")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@router.post("/success/")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})