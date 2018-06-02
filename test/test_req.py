import json
import unittest
import maintenance
import requests


class TestMaintenanceApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), {'hello': 'world'})


class Request_tests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_create_request_works(self):
        request = {"title": "laptop", "description": "laptop screen Repair",
                        "category": "maintenance"}
        res =  requests.post('http://localhost:5000/api/v1/request',json= request)
        self.assertEqual(res.status_code,201)

    def test_create_request_with_no_title(self):
        request = { "description": "laptop screen Repair",
                        "category": "maintenance"}
        res =  requests.post('http://localhost:5000/api/v1/request',json= request)
        self.assertEqual(res.status_code,400)
        self.assertEqual(json.loads(res.text)['message']['title'],"No request title provided")
    def test_create_request_with_no_description(self):
        request = {"title": "laptop",
                   "category": "maintenance"}
        res = requests.post('http://localhost:5000/api/v1/request', json= request)
        self.assertEqual(res.status_code,400)
        self.assertEqual(json.loads(res.text)['message']['description'],"No request description provided")
    def test_create_request_with_no_category(self):
        request = {"title": "laptop", "description": "laptop screen Repair"}
        res = requests.post('http://localhost:5000/api/v1/request',json=request)
        self.assertEqual(res.status_code,400)
        self.assertEqual(json.loads(res.text)['message']["category"], "Choose category")
    def test_update_request(self):
        request = {"title":"laptop","description":"laptop repair screen","category":"repair"}
        res = requests.post('http://localhost:5000/api/v1/request',json=request)
        post_id = json.loads(res.text)['request_id']
        request = {"title": "Desktop", "description": "Desktop repair screen", "category": "repair"}
        requests.put('http://localhost:5000/api/v1/request/' + str(post_id),json=request)
        updated = requests.get('http://localhost:5000/api/v1/request/' + str(post_id))
        self.assertEqual(json.loads(updated.text)['request_title'], "Desktop")
        self.assertEqual(json.loads(updated.text)['request_description'], "Desktop repair screen")

    def test_get_all(self):
        request =requests.get('http://localhost:5000/api/v1/request')
        self.assertEqual(request.status_code, 200)

if __name__ == "__main__":
    unittest.main()

