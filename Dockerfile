FROM python:3.10.2-alpine AS builder

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

# Allow to exec into docker container
RUN apk add --no-cache bash curl openssh iproute2 && \
    rm /bin/sh && \
    ln -s /bin/bash /bin/sh && \
    mkdir -p /app/.profile.d/ && \
    printf '#!/usr/bin/env bash\n\nset +o posix\n\n[ -z "$SSH_CLIENT" ] && source <(curl --fail --retry 7 -sSL "$HEROKU_EXEC_URL")\n' > /app/.profile.d/heroku-exec.sh && \
    chmod +x /app/.profile.d/heroku-exec.sh && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT api:'create_app()'
