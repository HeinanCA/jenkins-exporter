ARG FROM=python:3.11-alpine3.16
FROM ${FROM}

RUN adduser -D -u 1000 user \
    && mkdir /app \
    && chown user /app
WORKDIR /app/
COPY . .
RUN pip3 install -r requirements.txt

ARG PROM_EXPORTER_PORT=9118
ENV PROM_EXPORTER_PORT=${PROM_EXPORTER_PORT}
EXPOSE ${PROM_EXPORTER_PORT}
ENTRYPOINT [ "/usr/local/bin/python", "-u" ,"main.py" ]
