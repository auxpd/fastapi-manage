#!/bin/bash

read -p "worker name:" worker_name

celery multi start $worker_name -A tasks --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/%n%I.log" -l info
