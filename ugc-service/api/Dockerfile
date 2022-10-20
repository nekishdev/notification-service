### Build dependencies ###
FROM python:3.9 as builder

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG REQUIREMENTS_FILENAME=prod.txt

WORKDIR $APP_HOME

# Additional libs
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends libpq-dev gcc build-essential python-dev

COPY ./requirements ./requirements

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ./requirements/$REQUIREMENTS_FILENAME


### Final step ###
FROM python:3.9-slim

ARG EXPOSE_PORT=8000

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip \
    && pip install --no-cache /wheels/*

COPY . .

EXPOSE $EXPOSE_PORT

ENTRYPOINT []
#ENTRYPOINT ["python", "app.py"]