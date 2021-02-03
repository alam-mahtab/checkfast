FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install -r requirements.txt

EXPOSE 80

COPY ./testfast /main

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]