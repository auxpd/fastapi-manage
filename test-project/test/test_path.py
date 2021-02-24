import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    print('not find')
result = load_dotenv(encoding='utf-8')
print(result)

print(os.getenv('TEST_1'))

