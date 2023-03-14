FROM python:3.10

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

COPY rabbitmq /rabbitmq
RUN pip install /rabbitmq --no-cache-dir

WORKDIR /app
COPY bet_maker/requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir
COPY bet_maker/src /app/

CMD /wait && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080