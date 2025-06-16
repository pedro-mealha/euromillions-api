FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y postgresql-common && \
    apt-get install -y build-essential musl-dev && \
    pip3.12 install --prefix=/install -r requirements.txt --no-cache-dir

COPY . /app

# --

FROM tiangolo/uwsgi-nginx-flask:python3.12

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN apt-get install bash make

WORKDIR /app

COPY <<-"EOF" /etc/nginx/conf.d/default.conf
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=15r/m;

upstream gunicorn_app {
    server 127.0.0.1:3000;
}

server {
  listen 8080;
  listen [::]:8080;
  server_name localhost;

  location / {
    limit_req_status      429;
    limit_conn_status     429;
    limit_req             zone=mylimit;
    proxy_ssl_server_name on;
    proxy_read_timeout    1800;
    proxy_set_header      Host $host;
    proxy_set_header      X-Real-IP $remote_addr;
    proxy_set_header      X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header      X-Forwarded-Proto https;
    proxy_pass            http://gunicorn_app;
  }

  error_page 500 502 503 504 /50x.html;
  location = /50x.html {
    root /usr/share/nginx/html;
  }

  error_page 429 /429.html;
  location = /429.html {
    root /app;
  }
}
EOF

EXPOSE 8080

ENTRYPOINT ["sh", "/app/start.sh"]
