import json

import psycopg2
from psycopg2.extras import RealDictCursor


class MaintenanceDb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect (host='localhost', dbname='maintenanceAPI', user='postgres', password='LUG4Z1V4', port=5433)
        except:
            print("Unable to connect to the database")

    def getConnection(self):
        return self.connection

    # User
    def insert_user(self, UserDao):
        sql = """INSERT INTO users(username,email,password) VALUES (%s,%s,%s)"""
        # get connection
        cur = self.connection.cursor()
        # insert into database
        cur.execute(sql, (UserDao.username, UserDao.email, UserDao.password,))
        self.connection.commit()
        cur.close()

    def update_user(self, username,password,id):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        sql = """UPDATE users set username = %s , password = %s  
                    where id = %s"""
        cur.execute(sql,(username,password,id))
        updated_rows = cur.rowcount
        print(json.dumps(updated_rows,indent=2))
        self.connection.commit()
        cur.close()

    def delete_user(self, email):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("DELETE from users where email = %(email)s ",{'email':email})
        rows_deleted = cur.rowcount
        self.connection.commit()
        print(json.dumps(rows_deleted,indent=2))
        cur = self.connection.cursor (cursor_factory=RealDictCursor)

        cur.execute ("SELECT id,username,email,password from users ")
        rows = cur.fetchall ()
        print (json.dumps (rows, indent=2))
        return rows
        print('rows')

        cur.close()

    def get_user_by_email(self, email):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT id,username,email,password from users where email = %(email)s ", {'email': email})
        rows = cur.fetchall ()
        print(json.dumps(rows,indent=2))
        return rows

    def get_user_by_username(self, username):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute("""SELECT id,username,email,password from users 
                      where username = %(username)s """,
                     {'username': username})
        rows = cur.fetchall()
        print(json.dumps(rows,indent=2))
        return rows

    def get_all(self):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,username,email,password  from users")
        rows = cur.fetchall ()
        return rows

    def check_user_exist(self, email):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,username,email,password from users where email = %(email)s ", {'email': email})
        rows = cur.fetchone()
        if rows:
            return True
        else:
            return False
        cur.close()
    #requests data methods

    def insert_request(self, RequestDao):
        sql = """INSERT INTO requests(title,description,category) VALUES (%s,%s,%s)"""
        # get connection
        cur = self.connection.cursor()
        # insert into database
        cur.execute (sql, (RequestDao.title, RequestDao.description, RequestDao.category))
        self.connection.commit()
        cur.close()

    def update_request(self, title,description,author):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        sql = """UPDATE requests set title = %s , description = %s  
                    where author = %s"""
        cur.execute(sql,(title,description,author))
        updated_rows = cur.rowcount
        print(json.dumps(updated_rows,indent=2))
        self.connection.commit()
        cur.close()

    def delete_request(self, author):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("DELETE from users where author = %(author)s ",{'author':author})
        rows_deleted = cur.rowcount
        self.connection.commit()
        print(json.dumps(rows_deleted,indent=2))
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.close()

        cur.execute ("SELECT id,username,email,password from users ")
        rows = cur.fetchall ()
        print (json.dumps (rows, indent=2))
        return rows
        print('rows')
        cur.close()

    def get_request_by_id(self, email):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT id,username,email,password from users where email = %(email)s ", {'email': email})
        rows = cur.fetchall ()
        print(json.dumps(rows,indent=2))
        return rows
        cur.close()

    def get_request_by_author(self, username,password):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("""SELECT id,username,email,password from users 
                      where username = %(username)s and password = %(password)s""",
                     {'username': username,'password': password})
        rows = cur.fetchall ()
        print(json.dumps(rows,indent=2))
        return rows
        cur.close()

    def getall_requests(self):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT *  from requests")
        rows = cur.fetchall ()
        return rows

        # revoked tokens storage

    def add_token(self,jti):
        sql = "INSERT INTO revoked_tokens(jti) VALUES ('{0}')".format(jti)
        # get connection
        cur = self.connection.cursor ()
        # insert into database
        cur.execute (sql)
        self.connection.commit()
        cur.close()



