FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
expose 8000
CMD ["gunicorn", "backend.wsgi", "--timeout", "600"]