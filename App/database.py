
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

while True:
  try:
    conn = psycopg2.connect(host=settings.db_hostname, port=settings.db_port, database=settings.db_name, user=settings.db_username, password=settings.db_password, cursor_factory=RealDictCursor)

    cur = conn.cursor()
    print("Database connection was successfull")
  
    break
  except Exception as error: 
    print("Connecting to database failed")
    print("Error: ", error)
    time.sleep(2)


