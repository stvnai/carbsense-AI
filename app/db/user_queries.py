from app.db.connection import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def user_exists(username: str, email:str) -> bool:

    query= """
        SELECT id FROM users
        WHERE username = %s OR email = %s
        LIMIT 1

        """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username, email))
                return cur.fetchone() is not None
            
    except Exception as e:
        print(f"User exists: {e}")

        return True
    

def insert_user(username: str, email: str, password: str) -> bool:
    password_hash= generate_password_hash(password)

    query= """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)

    """
    
    try: 
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query,(username, email, password_hash))
                conn.commit()

        return True
    
    except Exception as e:
        print(f"Error creating user: {e}")

        return False
    
def auth_user(username:str, password:str) -> bool:

    query= """
        SELECT password_hash 
        FROM users
        WHERE username=%s
        LIMIT 1    
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                result = cur.fetchone()

                if result:
                    stored_hash= result["password_hash"]
                    return check_password_hash(stored_hash, password)
                else:
                    return False
                
    except Exception as e:
        print("Error during authentication.")
        return False
