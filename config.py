from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("KEY", "test_key") # замените 'test_key'!!!!!!!!!!!!!!!!!!
algorithm = os.getenv("ALGORITHM", "HS256")
db_name = os.getenv("DB_NAME", "data.db")