FROM debian:11.5-slim

WORKDIR /courier

ARG VERSION=7.4.0
RUN apt update && \
    apt install -y curl && \
    curl -L -s https://github.com/nyaruka/courier/releases/download/v$VERSION/courier_${VERSION}_linux_amd64.tar.gz | tar xz && \
    chmod +x courier && \
    mkdir /var/spool/courier

EXPOSE 8080
ENTRYPOINT ["./courier"]
