import os
from functools import lru_cache
from typing import List

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
	PROJECT_NAME: str = "test-project"

	LOG_LEVEL: str = 'DEBUG'  # TRACE, INFO, SUCCESS, WARNING, ERROR, CRITICAL ...

	API_V1_STR: str = "/api/v1"

	SECRET_KEY: str = "jymxRSTcLK7Y0AJrYVT12BGQ7HO7IvhXx5HM5_z55Xo"
	SALT_ROUNDS: int = 4

	# JWT expiration time
	ACCESS_TOKEN_EXPIRES_MINUTES: int = 1

	# Pagination
	PAGE_QUERY_PARAM: str = ''
	PAGE_SIZE_QUERY_PARAM: str = ''

	# Cross-domain request configuration
	BACKEND_CORS_ORIGINS: List = ["*"]

	# Database configuration
	MYSQL_USER: str = "dfc_user"
	MYSQL_PASS: str = "Aa1234"
	MYSQL_HOST: str = "10.210.120.226"
	MYSQL_DB: str = "dfc_bk"
	MYSQL_PORT: str = "3306"
	SQLALCHEMY_DATABASE_URI: str = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

	# Redis store address
	REDIS_STORAGE = "redis://127.0.0.1:6379/?password="

	TEST_1: int = 123
	TEST_2: list = []

	class Config:
		case_sensitive = True


@lru_cache(1)
def get_config():
	from dotenv import load_dotenv, find_dotenv
	if find_dotenv():
		logger.debug('找到env, 采用.env配置项目')
		load_dotenv(encoding='utf8')
		return Settings()
	else:
		dev_mode = os.getenv('DEV_MODE', 'test')
		if dev_mode == 'prod':
			logger.debug('识别生产模式, 自动请求生产环境env配置')
			os.environ['TEST_1'] = '88888'
			return Settings()
		else:
			logger.debug('识别测试模式, 自动请求测试环境env配置')
			os.environ['TEST_1'] = '666666'
			return Settings()


settings = get_config()
