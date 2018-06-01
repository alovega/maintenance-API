from flask import Flask ,jsonify,abort
from instance.config import app_config
from maintenance.models import Request
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    request1 = []
    request_1=Request("laptop","laptop screen Repair","maintenance")
    request_3=Request("window","window broken","maintenance")
    request1.append(request_1.add_request())
    request = set()
    request.add(request1)
    request1.append(request_3.add_request())

    @app.route('/api/v1/request', methods=['GET'])
    def get_all_requests():
        return jsonify({'request':request})
    @app.route('/api/v1/request/<int:request_id>', methods=['GET'])
    def get_request_by_id(request_id):
        request = [request for request in requests if request['id'] == request-id]
        if len(request) == 0:
            abort(404)
        return jsonify({'request':request[0]})


    return app
