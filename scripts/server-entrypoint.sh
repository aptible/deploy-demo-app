#! /usr/bin/env bash

sleep 3;
python -m migrations
python -m gunicorn app:app -b 0.0.0.0:$PORT --access-logfile -