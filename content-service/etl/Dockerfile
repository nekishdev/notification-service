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

# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

COPY --from=builder /opt/app/wheels /wheels

RUN pip install --upgrade pip \
     && pip install --no-cache /wheels/*

COPY entrypoint.sh /opt/entrypoint.sh

RUN sed -i 's/\r$//' /opt/entrypoint.sh \
    && chmod +x /opt/entrypoint.sh

COPY . .

ENTRYPOINT ["/opt/entrypoint.sh"]
