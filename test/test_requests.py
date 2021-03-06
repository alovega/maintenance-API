import json
import unittest

import psycopg2
from flask_restful import Api

from maintenance import create_app, HelloWorld, RequestUser, UserRegister


class Request_tests(unittest.TestCase):
    def setUp(self):
        try:
            self.connection = psycopg2.connect (host='localhost', dbname='test_db', user='postgres', password='LUG4Z1V4', port=5433)
        except:
            print("Unable to connect to the database")
        app = create_app("testing")
        app.config["Testing"] = True
        self.client = app.test_client()

    def test_hello_world(self):
        response = self.client.get('/')
        print(response)
        self.assertEqual(response.status_code,200)

    def test_create_request_works(self):
        res1 = {"username": "kevin", "password": "1234"}
        result = self.client.post ('/auth/login', json=res1)
        access_token = result.json['access_token']
        headers = {"Authorization": "Bearer {0}".format(access_token)}
        request = {"user_id":8,"title": "laptop", "description": "laptop screen Repair",
                   "category": "maintenance"}
        res = self.client.post('/users/requests', json=request, headers=headers)
        self.assertEqual(res.status_code, 201)

    def test_create_request_with_no_title(self):
        res1 = {"username": "kevin", "password": "1234"}
        result = self.client.post ('/auth/login', json=res1)
        access_token = result.json['access_token']
        headers = {"Authorization": "Bearer {0}".format (access_token)}
        request = {"user_id":8, "description": "laptop screen Repair",
                   "category": "maintenance"}
        res = self.client.post('/users/requests', json=request,headers=headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']['title'], "No request title provided")

    def test_create_request_with_no_description(self):
        res1 = {"username": "kevin", "password": "1234"}
        result = self.client.post ('/auth/login', json=res1)
        access_token = result.json['access_token']
        headers = {"Authorization": "Bearer {0}".format (access_token)}
        request = {"user_id":8,"title": "laptop",
                   "category": "maintenance"}
        res = self.client.post('/users/requests', json=request,headers=headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']['description'], "No request description provided")

    def test_create_request_with_no_category(self):
        res1 = {"username": "kevin", "password": "1234"}
        result = self.client.post ('/auth/login', json=res1)
        access_token = result.json['access_token']
        headers = {"Authorization": "Bearer {0}".format (access_token)}
        request = {"user_id":8,"title": "laptop", "description": "laptop screen Repair"}
        res = self.client.post('/users/requests', json=request,headers=headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']["category"], "Choose category")


    def test_get_all(self):
        res1 = {"username": "kevin", "password": "1234"}
        result = self.client.post ('/auth/login', json=res1)
        access_token = result.json['access_token']
        headers = {"Authorization": "Bearer {0}".format (access_token)}
        request = self.client.get('/requests/',headers=headers)
        self.assertEqual(request.status_code, 200)


if __name__ == "__main__":
    unittest.main()
