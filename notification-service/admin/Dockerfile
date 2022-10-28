FROM python:3.9.5-slim

# set work directory
WORKDIR /src

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
  
COPY ./src .

ENV SECRET_KEY ./.env

RUN ["python", "manage.py", "collectstatic", "--no-input", "--clear"]

COPY entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
