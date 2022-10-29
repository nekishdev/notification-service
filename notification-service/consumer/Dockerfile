### Build dependencies ###
FROM python:3.10 as builder

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

COPY ./requirements.txt .

RUN apt-get update && apt-get install libpq5 -y

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ./requirements.txt


### Final step ###
FROM python:3.10-slim

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

RUN apt-get update && apt-get install libpq5 -y
# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

# pip install
COPY requirements.txt requirements.txt
COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip \
    && pip install --no-cache /wheels/*

# entrypoint.sh
#COPY entrypoint.sh /opt/entrypoint.sh

#RUN sed -i 's/\r$//' /opt/entrypoint.sh \
#    && chmod +x /opt/entrypoint.sh

COPY . .

WORKDIR $APP_HOME/src

CMD []