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

    def delete_user(self, email):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE from users where email = %(email)s ", {'email': email})
        rows_deleted = cur.rowcount
        self.connection.commit()
        print(json.dumps(rows_deleted,indent=2))
        cur = self.connection.cursor (cursor_factory=RealDictCursor)

        cur.execute("SELECT id,username,email,password from users ")
        rows = cur.fetchall()
        print(json.dumps(rows, indent=2))
        return rows
        print('rows')
        cur.close()

    def get_user_by_username(self, username):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT id,username,email,password,is_admin from users 
                      where username = %(username)s """,
                     {'username': username})
        rows = cur.fetchall()
        return rows

    def get_all(self):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id,username,email,password  from users")
        rows = cur.fetchall ()
        return rows

    def update_to_admin(self,id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE users set is_admin = true  where id = {0}".format (id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        self.connection.commit()
        cur.close()
        return {"message" :"user is know  Admin"}

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
        sql = """INSERT INTO requests(user_id,title,description,category) VALUES (%s,%s,%s,%s) Returning *"""
        # get connection
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        # insert into database
        cur.execute(sql, (RequestDao.user_id,RequestDao.title, RequestDao.description, RequestDao.category))
        self.connection.commit()
        result2 = cur.fetchone()
        cur.close()
        return result2

    def update_request(self,title, description,category,id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        check="select approve  from requests where id = {0}".format(id)
        cur.execute(check)
        approved = cur.fetchone()
        if approved['approve']:
            cur.close()
            return -1

        sql = "UPDATE requests set title = '{0}' , description = '{1}', category = '{2}' where id = {3}".format(title, description, category,id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        self.connection.commit()
        cur.close()
        return updated_rows

    def delete_request(self, request_id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE from requests where request_id = %(request_id)s ",{'request_id': request_id})
        rows_deleted = cur.rowcount
        self.connection.commit()
        print(json.dumps(rows_deleted,indent=2))
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.close()

        cur.execute("SELECT id,username,email,password from users ")
        rows = cur.fetchall()
        print(json.dumps(rows, indent=2))
        return rows
        print('rows')
        cur.close()

    def get_request_by_user_id(self, user_id):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute("SELECT * from requests where user_id = %(user_id)s ", {'user_id': user_id})
        rows = cur.fetchall()
        return rows
        cur.close ()

    def get_request_by_request_id(self, id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * from requests where id = %(id)s ", {'id': id})
        rows = cur.fetchone()
        return rows
        cur.close()


    def getall_requests(self):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT *  from requests")
        rows = cur.fetchall()
        return rows
        cur.close()

    def admin_disapprove_request(self, id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE requests set approve = false  where id = {0}".format (id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        print(json.dumps (updated_rows, indent=2))
        self.connection.commit ()
        cur.close ()
        return updated_rows
    def admin_approve_request(self, id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE requests set approve = true  where id = {0}".format (id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        print (json.dumps (updated_rows, indent=2))
        self.connection.commit ()
        cur.close ()
        return updated_rows

    def admin_resolve_request(self,id):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        sql = "UPDATE requests set resolve = true  where id = {0}".format(id)
        cur.execute(sql)
        updated_rows = cur.rowcount
        print(json.dumps(updated_rows, indent=2))
        self.connection.commit()
        cur.close()
        return updated_rows

# revoked tokens storage

    def add_token(self, jti):
        sql = "INSERT INTO revoked_tokens(jti) VALUES ('{0}')".format(jti)
        # get connection
        cur = self.connection.cursor()
        # insert into database
        cur.execute(sql)
        self.connection.commit()
        cur.close()



