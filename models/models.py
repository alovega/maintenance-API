import psycopg2


class UserModels (object):
    def __init__(self):
        try:
            conn = psycopg2.connect (host='localhost', dbname='maintenanceAPI', user='postgres', password='LUG4Z1V4',
                                     port=5433)
            print ('Established')
        except:
            print ("Unable to connect to the database")

        cur = conn.cursor ()

    def insert_user(self, UserDao):
        sql = """INSERT INTO users(username,email,password) VALUES (%s,%s,%s)"""
        conn = psycopg2.connect (host='localhost', dbname='maintenanceAPI', user='postgres', password='LUG4Z1V4',
                                 port=5433)

        cur = conn.cursor ()

        cur.execute (sql, (UserDao.username, UserDao.email, UserDao.password))

        conn.commit ()

        cur.close ()
