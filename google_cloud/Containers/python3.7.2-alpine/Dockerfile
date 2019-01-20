FROM python:3.7.2-alpine

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY test.py /app
WORKDIR /app

CMD [ "python", "test.py" ]