FROM python:3.6-alpine
ENV TZ=America/Los_Angeles

RUN apk add --update --no-cache \
    alpine-sdk \
    bash \
    build-base \
    linux-headers \
    mysql-dev \
    openldap-dev \
    pcre \
    pcre-dev \
    python3 \
    python3-dev \
    py3-pip

ENV INSTALL_PATH /app
RUN mkdir -p ${INSTALL_PATH}
WORKDIR ${INSTALL_PATH}

COPY requirements.txt ${INSTALL_PATH}
RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r ./requirements.txt

COPY . ${INSTALL_PATH}

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
