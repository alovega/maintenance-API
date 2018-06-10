import json
import unittest
from maintenance import app

class Request_tests(unittest.TestCase):
    def setUp(self):
        app.config["Testing"] = True
        self.client = app.test_client()


    def test_hello_world(self):
        response = self.client.get('/')
        print(response)
        self.assertEqual(response.status_code,200)

    def test_create_request_works(self):
        request = {"title": "laptop", "description": "laptop screen Repair",
                   "category": "maintenance"}
        res = self.client.post('/api/v1/request', json=request)
        self.assertEqual(res.status_code, 201)

    def test_create_request_with_no_title(self):
        request = {"description": "laptop screen Repair",
                   "category": "maintenance"}
        res = self.client.post('/api/v1/request', json=request)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']['title'], "No request title provided")

    def test_create_request_with_no_description(self):
        request = {"title": "laptop",
                   "category": "maintenance"}
        res = self.client.post('/api/v1/request', json=request)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']['description'], "No request description provided")

    def test_create_request_with_no_category(self):
        request = {"title": "laptop", "description": "laptop screen Repair"}
        res = self.client.post('/api/v1/request', json=request)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message']["category"], "Choose category")

    def test_update_request(self):
        request = {"title": "laptop", "description": "laptop repair screen", "category": "repair"}
        res = self.client.post('/api/v1/request', json=request)
        post_id = res.json['request_id']
        request = {"title": "Desktop", "description": "Desktop repair screen", "category": "repair"}
        self.client.put('/api/v1/request/' + str(post_id), json=request)
        updated = self.client.get('/api/v1/request/' + str(post_id))
        self.assertEqual(updated.json['request_title'], "Desktop")
        self.assertEqual(updated.json['request_description'], "Desktop repair screen")

    def test_get_all(self):
        request = self.client.get('/api/v1/request')
        self.assertEqual(request.status_code, 200)


if __name__ == "__main__":
    unittest.main()
