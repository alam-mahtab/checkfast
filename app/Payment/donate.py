from fastapi import Depends,File, UploadFile, APIRouter,Request
from fastapi.templating import Jinja2Templates
import uuid, datetime
from app.talent.database import SessionLocal, engine, database
from starlette.responses import RedirectResponse
import razorpay
from fastapi.responses import HTMLResponse
from . import models,schemas
router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/payment/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
from random import randint
@router.post("/payment/")
async def home_pay(pay : schemas.PaymentCreate,request: Request):
    #id=None
    gid = randint(100000,1000000)
    gdate = datetime.datetime.now()
    print(router)
    query = models.Payment.__table__.insert().values(
        id = gid,
        name = pay.name,
        email = pay.email,
        amount= pay.amount,
        created_date = gdate)

    await database.execute(query)
    #id=pay.id
    # #url = router.url_path_for("pay"   ,id=models.Payment.id)
    # url = request.url_for("pay"   ,id=models.Payment.id)
    # print(url)
    # response = RedirectResponse(url=url)#id=models.Payment.id
    # return response
    return {
        **pay.dict(),
        "id" :gid,
        "created_at" : gdate,
    }
    #return templates.TemplateResponse("index.html", {"request": request})
import pandas as pd
@router.post("/pay/{id}",response_class=HTMLResponse)
#, methods=["post","get"])
async def pay(request: Request, id:str):
    #pay = models.Payment.__table__.select(models.Payment.amount).where(models.Payment.id==id)
    pay =  "SELECT payments.amount FROM payments WHERE payments.id ="+str(id)
    result = await database.execute(pay)
    print(pay)
    #print(pay.amount)
    df= pd.read_sql(pay,engine)
    print(df.amount.values)
    print("hello")
    print(df.shape[0])
    print("bye")
    # any = models.Payment.amount
    print(result)
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w","dcPlBgM8Fv7H2J1cYISFKC81"))
    payment = client.order.create({'amount' : int(10)*100, 'currency':'INR', 'payment_capture':'1'})
    return templates.TemplateResponse("pay.html", {"request": request, "payment":payment})

@router.get("/pay/{id}",response_class=HTMLResponse)
async def pay_me(request: Request, id:str):
    #pay = models.Payment.__table__.select(models.Payment.amount).where(models.Payment.id==id)
    
    pay =  "SELECT payments.amount FROM payments WHERE payments.id ="+str(id)
    result = await database.execute(pay)
    print(pay)
    #print(pay.amount)
    df= pd.read_sql(pay,engine)
    print(df.amount.values)
    print("hello")
    print(df.shape[0])
    print("bye")
    # any = models.Payment.amount
    print(result)
    client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w","dcPlBgM8Fv7H2J1cYISFKC81"))
    payment = client.order.create({'amount' : int(df.amount.values)*100, 'currency':'INR', 'payment_capture':'1'})
    return templates.TemplateResponse("pay.html", {"request": request, "payment":payment})

@router.get("/success/")
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})