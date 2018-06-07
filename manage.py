
import psycopg2

try:
    conn = psycopg2.connect(host='localhost',dbname='maintenanceAPI',user='postgres',password='LUG4Z1V4', port=5433)
    print('Established')
    def create_table():

        commands = (
            """
            CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, 
            email VARCHAR(80) NOT NULL, password VARCHAR(80) NOT NULL, is_admin VARCHAR(40) 
            DEFAULT FALSE NOT NULL)""",
            """
            CREATE TABLE IF NOT EXISTS requests(id SERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL,
            description  VARCHAR(100) NOT NULL, category VARCHAR(40) NOT NULL,author INT NOT NULL,
            FOREIGN KEY (author) REFERENCES users(id) ON DELETE CASCADE) 
            """)
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
