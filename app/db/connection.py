import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():


    return psycopg2.connect(
        dbname= os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASS"),
        host= os.getenv("DB_HOST"),
        port= os.getenv("DB_PORT"),
        cursor_factory=RealDictCursor

    )