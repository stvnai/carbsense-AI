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


try:
    ENGINE= get_sqlalchemy_engine()
except Exception as e:
    print(f"Something goes wrong connecting with database: {e}")
    ENGINE= None


def user_exists(username: str, email:str, engine:Engine=ENGINE) -> bool:

    """
    Description:
    -----
        Check if the actual user or password already exists in database.
    
    :param Engine engine: sqlalchemy engine.
    :param str username: username.
    :param str email: user email.
    :return bool|None: Bool.
    """

    if engine is None:
        print("No database engine available.")
        return False

    query= text(
        """
            SELECT id 
            FROM users
            WHERE username = :username OR email = :email
            LIMIT 1
        """
    )

    values= {"username": username,
             "email": email}
    
    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_id= result.scalar_one_or_none()

        if user_id:
            return True
        else:
            return False

    except Exception as e:
        return False


def insert_user(username: str, email: str, password: str, engine:Engine=ENGINE) -> bool:

    """
    Description
    -----
        Inserts new user into database.
        
        :param str username:
        :param str email:
        :param str password:
        return bool:
    """

    if engine is None:
        print("No database engine available.")
        return None

    password_hash= generate_password_hash(password)


    query= text(
        """
            INSERT INTO users (username, password_hash, email)
            VALUES (:username, :password_hash, :email)
        """
    )

    values= {
        "username":username,
        "password_hash":password_hash,
        "email":email,
    }
    
    try: 
        with engine.begin() as conn:
            conn.execute(query, values)  
            return True
    
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def auth_user(username:str, password:str, engine: Engine= ENGINE) -> bool:

    if engine is None:
        print("No database engine available")
        return None

    query= text(
        """
            SELECT id, password_hash
            FROM users
            WHERE username = :username
            LIMIT 1
        """
    )

    values= {"username": username}

    try:

        with engine.connect() as conn:

            result= conn.execute(query, values)
            user_data= result.fetchone()

            if user_data:

                user_id= user_data[0]
                stored_hash= user_data[1]
                if check_password_hash(stored_hash, password):
                    return user_id
            else:
                return None
                
    except Exception as e:
        print(f"Error during authentication: {e}.")
        return None



def get_user_by_id(user_id, engine:Engine=ENGINE):

    if engine is None:
        print("No database engine available")
        return None
    
    query= text(
        """
        SELECT id, username
        FROM users
        WHERE id = :id        
        """
    )

    values= {"id": user_id}

    try:
        with engine.connect() as conn:
            result= conn.execute(query, values)
            user_data= result.fetchone()
            print(user_data)
            return user_data
        
    except Exception as e:
        print(f"Error retrieving data from user: {e}")
        return None
