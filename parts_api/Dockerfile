FROM python:3.9

#ADD . .
COPY ./src /app/src
COPY ./requirements.txt /app


RUN pip install  -r  app/requirements.txt
EXPOSE 8000

CMD ["uvicorn", "app.src.main:app", "--host=0.0.0.0" , "--port=80", "--reload"]