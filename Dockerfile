FROM python:3.11.2-alpine AS builder

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --prefix=/install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /app

# --

FROM builder

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN apk add --no-cache bash make

WORKDIR /app

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 api:'create_app()'
