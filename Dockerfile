FROM python:3.9.7-alpine AS builder

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3.9 install --prefix=/install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /app

# --

FROM builder

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

WORKDIR /app

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT api:'create_app()'
