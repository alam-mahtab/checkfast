FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt ./

COPY ./app /app/app
COPY ./static /static

RUN pip install -r requirements.txt

EXPOSE 15400


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]