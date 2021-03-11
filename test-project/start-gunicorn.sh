#!/bin/bash
read -p "dev_mode: " dev_mode
read -p "server_port: " server_port
gunicorn -b 0.0.0.0:$server_port -w 1 -k uvicorn.workers.UvicornWorker -e DEV_MODE=$dev_mode --preload main:app
