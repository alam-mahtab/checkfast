FROM python3.7

RUN pip install -r requirements.txt

EXPOSE 15400

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]