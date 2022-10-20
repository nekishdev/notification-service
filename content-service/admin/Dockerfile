# Builder step
FROM python:3.10-slim as builder

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Additional libs
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends libpq-dev gcc build-essential python-dev

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /opt/app/wheels -r requirements.txt

# Final step
FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

COPY run_uwsgi.sh /opt/run_uwsgi.sh
COPY runserver.sh /opt/runserver.sh
COPY --from=builder /opt/app/wheels /wheels

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install --no-cache /wheels/* \
     && sed -i 's/\r$//' /opt/run_uwsgi.sh /opt/runserver.sh

COPY . .

ENTRYPOINT []
