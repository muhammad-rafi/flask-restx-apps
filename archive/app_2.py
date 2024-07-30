from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, fields, reqparse, marshal, model
from devices import devices_dict
import json

app = Flask(__name__)
api_ver = 'v1'
blueprint = Blueprint('api', __name__, url_prefix=f'/api/{api_ver}')

api = Api(
    blueprint, 
    version = '1.0',
    title = 'CISCO ALWAYS-ON SANDBOXES INVENTORY APIs',
    description = 'FLASK RESTX API APP FOR THE CISCO ALWAYS-ON SANDBOXES INVENTORY',
    default = 'REST APIs Endpoints', 
    default_label = 'Swagger APIs for Cisco Always-on Sandboxes',
    prefix = '/',
    doc = '/docs')

app.register_blueprint(blueprint)

device_model = api.model(
    "device",
    {
        'username': fields.String(required=True, description='username', default='device username'),
        'password': fields.String(required=True, description='password', default='device password'),
        'protocol': fields.String(required=True, description='protocol', default='ssh'),
        'port': fields.Integer(required=True, description='port', default=22),
        'os_type': fields.String(required=True, description='os_type', default='iosxe'),
    },
)

# Dummy data
devices = devices_dict

# # GET /devices
# @api.route('/devices')
# class Devices(Resource):
#     def get(self):
#         return jsonify(devices)

@api.route('/devices')
class Devices(Resource):
    def get(self):
        device_list = [{'id': device_id, **device} for device_id, device in devices.items()]
        return jsonify(device_list)
    
# GET /devices/{id}
@api.route('/devices/<int:device_id>')
class Device(Resource):
    def get(self, device_id):
        if device_id not in devices:
            return {'message': 'Device not found'}, 404
        return jsonify(devices[device_id])

    # DELETE /devices/{id}
    def delete(self, device_id):
        if device_id not in devices:
            return {'message': 'Device not found'}, 404
        del devices[device_id]
        return '', 204

    # PUT /devices/{id}
    @api.expect(device_model)
    def put(self, device_id):
        if device_id not in devices:
            return {'message': 'Device not found'}, 404
        data = api.payload
        devices[device_id] = {
            'username': data['username'],
            'password': data['password'],
            'protocol': data['protocol'],
            'port': data['port'],
            'os_type': data['os_type']
        }
        return devices[device_id], 200

# POST /devices
@api.route('/devices')
class CreateDevice(Resource):
    @api.expect(device_model)
    def post(self):
        data = api.payload
        new_device_id = max(devices.keys()) + 1
        devices[new_device_id] = {
            'username': data['username'],
            'password': data['password'],
            'protocol': data['protocol'],
            'port': data['port'],
            'os_type': data['os_type']
        }
        return devices[new_device_id], 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    