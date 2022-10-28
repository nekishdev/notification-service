### Build dependencies ###
FROM python:3.10 as builder

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

# For orjson package
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /opt/rustup.rs \
#    && sh /opt/rustup.rs -y --default-toolchain nightly \
#    && . "$HOME/.cargo/env"

COPY ./requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r ./requirements.txt


### Final step ###
FROM python:3.10-slim

ENV APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

# Install netcat (nc)
RUN apt-get -y update \
    && apt-get install -y netcat

# pip install
COPY requirements.txt requirements.txt
COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip \
    && pip install --no-cache /wheels/*

# entrypoint.sh
COPY entrypoint.sh /opt/entrypoint.sh

RUN sed -i 's/\r$//' /opt/entrypoint.sh \
    && chmod +x /opt/entrypoint.sh

COPY . .

WORKDIR $APP_HOME/src

ENTRYPOINT ["/opt/entrypoint.sh"]

CMD []