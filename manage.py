
import psycopg2

try:
    conn = psycopg2.connect(host='localhost',dbname='maintenanceAPI',user='postgres',password='LUG4Z1V4', port=5433)
    print('Established')
    def create_table():

        commands = (
            """
            CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username VARCHAR NOT NULL UNIQUE, 
            email VARCHAR(80) NOT NULL UNIQUE, password VARCHAR NOT NULL, is_admin VARCHAR(40) 
            DEFAULT FALSE NOT NULL)""",
            """
            CREATE TABLE IF NOT EXISTS requests(id SERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL,
            description  VARCHAR(100) NOT NULL, category VARCHAR(40) NOT NULL,approve VARCHAR(40) 
            DEFAULT FALSE, disapprove VARCHAR(40) DEFAULT FALSE,RESOLVE VARCHAR(40) DEFAULT FALSE, 
            user_id INTEGER  REFERENCES users(id)) 
            """,
            """CREATE TABLE IF NOT EXISTS 
             revoked_tokens(id SERIAL PRIMARY KEY, jti VARCHAR(120) )""")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()

except:
    print ("I am unable to connect to the database")


if __name__ == '__main__':
    create_table()
