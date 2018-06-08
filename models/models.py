import json

import psycopg2
from psycopg2.extras import RealDictCursor


class MaintenanceDb (object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect (host='localhost', dbname='maintenanceAPI'
                                                , user='postgres', password='LUG4Z1V4', port=5433)
            print ('Established')
        except:
            print ("Unable to connect to the database")

    # User
    def insert_user(self, UserDao):
        sql = """INSERT INTO users(username,email,password) VALUES (%s,%s,%s)"""
        # get connection
        cur = self.connection.cursor ()
        # insert into database
        cur.execute (sql, (UserDao.username, UserDao.email, UserDao.password))
        self.connection.commit ()
        cur.close ()

    def update_user(self, UserDao):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        sql = """UPDATE users set username = %s or password = %s where email = %(email)s"""
        cur.execute(sql,(UserDao.username, UserDao.password))
        self.connection.commit ()
        cur.close ()

    def delete_user(self, email):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("DELETE from users where email = %(email)s ",{'email':email})
        rows = cur.commit()
        print(json.dumps(rows,indent=2))


    def get_user_by_email(self, email):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT id,username,email,password from users where email = %(email)s ", {'email': email})
        rows = cur.fetchall ()
        print(json.dumps(rows,indent=2))
        return rows

    def get_user_by_password_and_name(self, username,password):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("""SELECT id,username,email,password from users 
                      where username = %(username)s and password = %(password)s""",
                     {'username': username,'password': password})
        rows = cur.fetchall ()
        print(json.dumps(rows,indent=2))
        return rows

    def getAll(self):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT id,username,email,password  from users")
        rows = cur.fetchall ()
        return rows


dao = MaintenanceDb ()
dao.update_user('amanda@hotmail.com')
