FROM debian:11.5-slim

WORKDIR /rp-indexer

ARG VERSION=7.4.0
RUN apt update && \
    apt install -y curl && \
    curl -L -s https://github.com/nyaruka/rp-indexer/releases/download/v$VERSION/rp-indexer_${VERSION}_linux_amd64.tar.gz | tar xz && \
    chmod +x rp-indexer

ENTRYPOINT ["./rp-indexer"]
