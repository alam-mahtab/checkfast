from fastapi import Depends,File, UploadFile, APIRouter,Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid, datetime
from app.talent.database import SessionLocal, engine, database
from starlette.responses import RedirectResponse
import sqlalchemy
import razorpay
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.authentication import schemas, models
from app.authentication.models import Course
from app.All_Course import crud
from .models import Payment
from app.authentication.models import Paid
router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
from random import randint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import pandas as pd

#client = razorpay.Client(auth=("rzp_test_AZImZBA0Ypgwni", "amS1t8KL21wnsFyh1cFHKfXb")) 
client = razorpay.Client(auth=("rzp_live_7Wz67232paIYjD","WjSsY2oGGw6HhZbXqsbcsRnT"))

@router.get("/pay/")#,response_class=HTMLResponse)
async def pay_me(request: Request, id:int, client_id:str, db: Session = Depends(get_db)):
    # bought_course = crud.check_duplicacy(db,client_id,id)
    # print(bought_course)
    # if bought_course is not None:
    #     raise HTTPException(status_code=400,detail="You already bought this course")
    check = "Select * From paids WHERE course_id ="+str(id)+" and client_id = '"+str(client_id)+"'"
    df1 = pd.read_sql(check,engine)
        #df = pd.read_sql(query, engine)
    print(df1)
    if df1.empty:
        pay =  "SELECT courses.price FROM courses WHERE courses.id ="+str(id)
        result = await database.execute(pay)
        gid = randint(100000,1000000)
        rec = ("paycd"+str(gid))
        gdate = datetime.datetime.now()
        df= pd.read_sql(pay,engine)
        payment = client.order.create({'amount' : int(df.price.values)*100, 'currency':'INR', 'receipt': "paycd"+str(gid),'payment_capture':'1'})
        query = Payment.__table__.insert().values(
            #id = str(gid),
            pay_id = payment['id'],
            amount = str(payment['amount']),
            currency = payment['currency'],
            receipt = payment['receipt'],
            status = payment['status'],
            pay_createdat = str(payment['created_at']),
            created_date = gdate,
            clients_id= client_id,
            courses_id = id)
        await database.execute(query)
        return templates.TemplateResponse("index.html", {"request": request, "payment":payment})
    else:
        raise HTTPException(status_code=400,detail="You already bought this course")

@router.get("/payments")
async def get_payment():
    count = 2
    skip = 1

    resp = client.order.fetch_all()
    return resp
# Get Payment Id client = razorpay.Client(auth=("rzp_test_cfbr43uRZAs35w", "dcPlBgM8Fv7H2J1cYISFKC81")
# @router.post("/pay/{id}/charge/")
# async def get_payment_by_id(request: Request, order_id:str):
    
#     client = razorpay.Client(auth=("rzp_test_AZImZBA0Ypgwni", "amS1t8KL21wnsFyh1cFHKfXb"))

#     order_id = order_id

#     resp = client.order.fetch(order_id)
#     return resp
@router.get("/payments/:id/payments")
async def get_all_payment_by_id(request: Request, order_id:str):
    
    #client = razorpay.Client(auth=("rzp_test_AZImZBA0Ypgwni", "amS1t8KL21wnsFyh1cFHKfXb"))

    order_id = order_id

    resp = client.order.fetch(order_id)
    return resp

@router.post("/pay/charge/")
async def success(request: Request,razorpay_payment_id:str, db: Session = Depends(get_db)):
    gdate = datetime.datetime.now()
    payment_id = razorpay_payment_id
    abc = client.order.fetch(payment_id)
    query = "Update payments SET status = 'paid' Where pay_id = '"+str(payment_id)+"'"
    db.execute(query)
    db.commit()
    query1 = "Select courses_id, clients_id from payments where pay_id = '"+str(payment_id)+"'"
    df= pd.read_sql(query1,engine)
    a = (df.clients_id.values)
    c = a[0]
    query2 = Paid.__table__.insert().values(
        payment_id = str(payment_id),
        created_date = gdate,
        client_id = c,
        course_id = int(df.courses_id.values))
    await database.execute(query2)

    return templates.TemplateResponse("success.html", {"request": request})

# @router.get("/success")
# async def success_(request: Request, db: Session = Depends(get_db)):
#     payment_id = 'order_GwvU8kgoH1DFgu'
#     abc = client.order.fetch(payment_id)
#     query = "Update payments SET status = 'paid' Where pay_id = '"+str(payment_id)+"'"
#     a = db.execute(query)
#     b = db.commit()
#     print(a)
#     print(b)
#     query1 = "Select courses_id, clients_id from payments where pay_id = '"+str(payment_id)+"'"
#     result = database.execute(query1)
#     df= pd.read_sql(query1,engine)
#     a = (df.clients_id.values)
#     c = a[0]
#     # listToStr = ''.join([str(elem) for elem in a])
#     # print(listToStr)
#     b = int(df.courses_id.values)
#     print(a,b,c)
#     query2 = Paid.__table__.insert().values(
#         payment_id = str(payment_id),
#         client_id = c,
#         course_id = int(df.courses_id.values))
#     await database.execute(query2)
    
#     return templates.TemplateResponse("success.html", {"request": request})