FROM python:3.14
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y gcc libpq-dev python3-psycopg2
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt && pip install psycopg[binary]
ADD . /code/
expose 8000
CMD ["gunicorn", "backend.wsgi", "--timeout", "600", "-b", "0.0.0.0"]