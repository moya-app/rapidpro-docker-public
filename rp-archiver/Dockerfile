FROM debian:11.5-slim

WORKDIR /rp-archiver

ARG VERSION=7.4.0
RUN apt update && \
    apt install -y curl && \
    curl -L -s https://github.com/nyaruka/rp-archiver/releases/download/v$VERSION/rp-archiver_${VERSION}_linux_amd64.tar.gz | tar xz && \
    chmod +x rp-archiver

ENTRYPOINT ["./rp-archiver"]
