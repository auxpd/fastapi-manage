import os
from typing import List

from dotenv import load_dotenv, find_dotenv

from pydantic import BaseSettings


class Settings(BaseSettings):
	PROJECT_NAME: str = "test-project"

	LOG_LEVEL: str = 'DEBUG'  # TRACE, INFO, SUCCESS, WARNING, ERROR, CRITICAL ...

	API_V1_STR: str = "/api/v1"

	SECRET_KEY: str = "jymxRSTcLK7Y0AJrYVT12BGQ7HO7IvhXx5HM5_z55Xo"
	SALT_ROUNDS: int = 4

	# JWT expiration time
	ACCESS_TOKEN_EXPIRES_MINUTES: int = 1

	# pagination
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
	SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

	# Redis store address
	REDIS_STORAGE = "redis://127.0.0.1:6379/?password="

	TEST_1: int = 123
	TEST_2: list = []

	# def __new__(cls, *args, **kwargs):
	# 	obj = object.__new__(cls)
	# 	if find_dotenv():
	# 		load_dotenv(encoding='utf-8')
	# 		for key in obj.__fields__:
	# 			env_value = os.getenv(key)
	# 			if env_value:
	# 				obj.__setattr__(key, env_value)
	# 	else:
	# 		...  # web_request
	# 	return obj

	class Config:
		case_sensitive = True


settings = Settings()
