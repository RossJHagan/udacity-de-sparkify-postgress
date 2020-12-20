import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("POSTGRES_HOST")
db_default_schema = os.getenv("POSTGRES_DEFAULT_DB")
db_create_user = os.getenv("POSTGRES_USER_CREATE_DB_PRIVILEGES")
db_create_pass = os.getenv("POSTGRES_PASSWORD_CREATE_DB_PRIVILEGES")

data_store_schema = os.getenv("DATA_STORE_SCHEMA")
data_store_user = os.getenv("DATA_STORE_USER")
data_store_pass = os.getenv("DATA_STORE_PASSWORD")
