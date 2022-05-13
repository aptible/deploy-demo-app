#! /usr/bin/env bash

 # wait for server to start
sleep 3;
# run migrations
python -m migrations
# run server
python -m gunicorn app:app -b 0.0.0.0:$PORT --access-logfile -