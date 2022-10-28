FROM python:3.9.5-slim

# set work directory
WORKDIR /src

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

ENV SECRET_KEY ./.env

#RUN ["mkdir", "static"]

# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

COPY entrypoint.sh /opt/entrypoint.sh

RUN sed -i 's/\r$//' /opt/entrypoint.sh \
    && chmod +x /opt/entrypoint.sh

RUN ["python", "manage.py", "collectstatic", "--no-input", "--clear"]

ENTRYPOINT ["/opt/entrypoint.sh"]

CMD []