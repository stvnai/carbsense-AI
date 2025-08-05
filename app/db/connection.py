import os
from sqlalchemy import create_engine, Engine, text
from werkzeug.security import generate_password_hash, check_password_hash


def get_sqlalchemy_engine() -> Engine:
    """
    Description:
    -----
        Returns a sqlalchemy engine connected to PostgreSQL database.

    :return Engine: sqlalchemy engine.

    """

    dbname= os.getenv("DB_NAME")
    user= os.getenv("DB_USER")
    password= os.getenv("DB_PASS")
    host= os.getenv("DB_HOST")
    port= os.getenv("DB_PORT")

    db_url= f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

    engine= create_engine(
        db_url,
        echo= False,
        future= True,
        pool_size= 5,
        max_overflow= 2,
        pool_timeout= 60,
        pool_pre_ping= True, 
        pool_recycle= 3600
    )
    
    return engine

engine= get_sqlalchemy_engine()

if engine is not None:
    print("connected")
else:
    print("not connnected")