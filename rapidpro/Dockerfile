FROM python:3.9.14

WORKDIR /rapidpro
RUN apt update && \
    apt install -y git nodejs npm libgdal28

ARG VERSION=7.4.2
RUN git clone --depth 1 --branch v$VERSION https://github.com/rapidpro/rapidpro . && \
    pip install poetry gunicorn && \
    poetry install && \
    npm install -g less coffeescript && \
    npm install -y

EXPOSE 8080
COPY ./cmd.sh /cmd.sh

CMD ["/cmd.sh"]
