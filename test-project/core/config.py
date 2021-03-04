import os
from functools import lru_cache
from typing import List

import requests
from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
	PROJECT_NAME: str = "test-project"

	LOG_LEVEL: str = 'DEBUG'  # TRACE, INFO, SUCCESS, WARNING, ERROR, CRITICAL ...

	API_V1_STR: str = "/api/v1"

	SECRET_KEY: str = "jymxRSTcLK7Y0AJrYVT12BGQ7HO7IvhXx5HM5_z55Xo"
	SALT_ROUNDS: int = 4

	# JWT expiration time
	ACCESS_TOKEN_EXPIRES_MINUTES: int = 30

	# Pagination
	PAGE_QUERY_PARAM: str = ''
	PAGE_SIZE_QUERY_PARAM: str = ''

	# Cross-domain request configuration
	BACKEND_CORS_ORIGINS: List = ["*"]

	# Database configuration
	MYSQL_USER: str = "test_user"
	MYSQL_PASS: str = "123456"
	MYSQL_HOST: str = "10.210.120.226"
	MYSQL_DB: str = "test_db"
	MYSQL_PORT: str = "3306"
	SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

	# Redis store address
	REDIS_STORAGE_HOST: str = '127.0.0.1'
	REDIS_STORAGE_PORT: str = '6379'
	REDIS_STORAGE_PASS: str = ''
	REDIS_STORAGE = f"redis://{REDIS_STORAGE_HOST}:{REDIS_STORAGE_PORT}/?password={REDIS_STORAGE_PASS}"

	# RateLimitBackend
	RATE_LIMIT_REDIS_BACKEND_HOST: str = '127.0.0.1'
	RATE_LIMIT_REDIS_BACKEND_PORT: str = '6379'
	RATE_LIMIT_REDIS_BACKEND_DB: str = '12'
	RATE_LIMIT_REDIS_BACKEND_PASS: str = 'Aa1234'

	# Celery broker & backend
	CELERY_BROKER: str = 'redis://:Aa1234@127.0.0.1:6379/7'
	CELERY_BACKEND: str = 'redis://:Aa1234@127.0.0.1:6379/8'

	TEST_1: int = 123
	TEST_2: list = []

	class Config:
		case_sensitive = True


@lru_cache(1)
def get_config():
	""" 优先采用.env, 其次请求云端配置, 最后才是是config.py里的值 """
	devops_server_host = 'http://127.0.0.1'
	api_key = ''
	app = ''
	from dotenv import load_dotenv, find_dotenv
	if find_dotenv():
		logger.debug('找到env, 采用.env配置项目')
		load_dotenv(encoding='utf8')
		return Settings()
	else:
		dev_mode = os.getenv('DEV_MODE', None)
		assert dev_mode in ['test', 'prod']
		devops_api = f'{devops_server_host}/api/apis/config/?apiKey={api_key}&app={app}&env={dev_mode}&format=json'
		if dev_mode == 'prod':
			logger.debug('识别生产模式, 自动请求生产环境env配置')
			requests.get()
			os.environ['TEST_1'] = '88888'
			return Settings()
		else:
			logger.debug('识别测试模式, 自动请求测试环境env配置')
			os.environ['TEST_1'] = '666666'
			return Settings()


settings = get_config()
