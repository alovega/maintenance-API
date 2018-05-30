import unittest
from maintenance import create_app
from maintenance.models import User
import json

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()

        self.request = {"request_title":"laptop" ,"request_description":"laptop screen Repair",
        "request_category":"maintenance"
        }
    def test_request_creation(self):
        res = self.client.post('/api/v1/request',data=json.dumps(dict(request_title="laptop",
        request_description="laptop screen Repair",
        request_category="repair")),content_type="application/json")
        response = json.loads(res.data.decode())
        self.assertIn("Request Created",response["message"])
             # self.assertEqual(res.status_code,201)
             # self.assertIn('laptop screen Repair',str(res.data))

    def test_api_can_get_all_requests(self):
        create = self.client.post('/api/v1/request',data=json.dumps(dict(request_title="laptop",
        request_description="laptop screen Repair",
        request_category="repair")),content_type="application/json")
        res = self.client.get('/api/v1/request')
        response = json.loads(create.data.decode())
        created_request = response[0]
        self .assertEqual(created_request["request_title"],"laptop")

    def test_api_can_get_request_by_id(self):
        create = self.client.post("/api/v1/request",data=json.dumps(dict(request_title="laptop",
        request_description="laptop screen Repair",
        request_category="repair")),content_type="application/json")
        res = self.client.get('/api/v1/request/0')
        response = json.loads(res.data.decode())
        self.assertIn("laptop screen Repair",response["request_description"])

    def test_api_can_update_request(self):
        res = self.client.post('api/v1/request/0', data=json.dumps(dict(request_title="laptop",
        request_description="laptop screen Repair",request_category="repair")),content_type="application/json")
        res = self.client.put('api/v1/request/0', data=json.dumps(dict(request_title="Screen",
        request_category="maintenance")), content_type="application/json")
        result = self.client.get('/api/v1/request/0')
        self.assertIn("screen", response["title"])
