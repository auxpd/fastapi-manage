#!/bin/bash

celery -A tasks.my_tasks worker -l info
