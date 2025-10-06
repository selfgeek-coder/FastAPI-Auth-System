from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("KEY")
algorithm = os.getenv("ALGORITHM")