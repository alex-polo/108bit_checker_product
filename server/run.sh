#!/bin/bash
gunicorn src.main:app \
  --workers 3 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8080 \
  --log-level="info" \
  --log-file "/logs/gunicorn.log" \
  --access-logfile "/logs/access.log" \
  --certfile='/etc/letsencrypt/live/api.108bit.ru/fullchain.pem' \
  --keyfile='/etc/letsencrypt/live/api.108bit.ru/privkey.pem'