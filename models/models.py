import psycopg2
from instance.config import config
class UserModels(object):
    def connect(self):
        conn = None
        try:
            params = config()

            print('connecting to the PostgreSQL models')
            conn = psycopg2.connect(**params)

            cur = conn.cursor()

            print('PostgreSQL models version:')
            cur.execute('SELECT version()')

            db_version = cur.fetchone()
            print(db_version)
            cur.close()
        except (Exception, psycopg2.DataError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed')

    def create_tables(self):
        commands = ("""
      CREATE TABLE IF NOT EXIST USER(
      id SERIAL PRIMARY KEY NOT NULL,
      name VARCHAR(70) NOT NULL,
      email VARCHAR    NOT NULL UNIQUE,
      is_admin BOOLEAN DEFAULT FALSE
      password VARCHAR NOT NULL

        )""",
                    """CREATE TABLE IF NOT EXIST REQUEST(
                       user_id SERIAL PRIMARY KEY NOT NULL,
                       title VARCHAR(30) NOT NULL,
                       description VARCHAR NOT NULL,
                       category VARCHAR NOT NULL,
                       approve  BOOLEAN  DEFAULT FALSE NOT NULL,
                       disapprove  DEFAULT,
                       resolve  FALSE DEFAULT
                       posted_by SERIAL references USER(ID)
                        )""")
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()

    def insert_user(self, UserDao):
        sql = """INSERT INTO  user(email,username,password) VALUES (%s,%s,%s) RETURNING id"""
        conn = None
        user_id = None
        params = config()

        conn = psycopg2.connect(**params)

        cur = conn.cusor()

        cur.excecute(sql, (UserDao.email, UserDao.username, UserDao.password))
        id = cur.fetchone()[0]

        conn.commit()

        cur.close()

        return user_id
