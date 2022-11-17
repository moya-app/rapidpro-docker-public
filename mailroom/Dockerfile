FROM debian:11.5-slim

WORKDIR /mailroom

ARG VERSION=7.4.1
RUN apt update && \
    apt install -y curl && \
    curl -L -s https://github.com/nyaruka/mailroom/releases/download/v$VERSION/mailroom_${VERSION}_linux_amd64.tar.gz | tar xz && \
    chmod +x mailroom

EXPOSE 8090
ENTRYPOINT ["./mailroom"]
