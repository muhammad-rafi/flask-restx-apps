from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, fields, reqparse, marshal, model
from devices import devices_list
import json

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    version="1.0",
    title="Cisco Sandbox APIs",
    description="A simple Devices API",
    doc = '/docs'
)

# ns = api.namespace("Sandbox Devices APIs", description="REST API Operations")

device_model = api.model(
    "device", {
        # "id": fields.Integer(required=False, description='id', default='0'),
        "host": fields.String(required=True, description='HostName/IP', default='cml-core01.example.com'),
        'username': fields.String(required=True, description='username', default='admin'),
        'password': fields.String(required=True, description='password', default='mYsEcrEt'),
        'protocol': fields.String(required=True, description='protocol', default='ssh'),
        'port': fields.Integer(required=True, description='port', default=22),
        'os_type': fields.String(required=True, description='os_type', default='iosxe'),
    },
)

device_post_model = api.model('devices', {
    'devices': fields.List(fields.Nested(device_model), required=True, description='List of devices')
})

device_resp_model = device_model.clone(
    'devices', {
        'id': fields.Integer(required=True, description='id'),
        },
    )

api.models[device_resp_model.name] = device_resp_model

response_model = api.model(
    "response", {
        "message": fields.String(required=True),
        "status_code": fields.Integer(required=True)
        },
    )

def marshal_resp(message, response_code, response_model):
    """ Marshal the api response."""
    return (
        marshal (
            {
            "message": message, 
            "status_code": response_code
             }, 
            response_model
        )
    )

# @ns.route("/devices")
class Devices(Resource):
    """Shows list of current devices in the database, 
    and lets you POST to add new device(s)"""
    
    @api.marshal_list_with(device_resp_model, code=200, description="List of device", envelope='devices')
    def get(self):
        """Get the current devices"""
        # return {"devices": devices}
        return devices_list

    # @api.marshal_with(response_model, code=201, description="Add a new device")
    @api.marshal_with(response_model)
    @api.expect(device_post_model, validate=True)
    def post(self):
        """Add a new device"""
        # new_device = api.payload
        # # del new_device['id']
        
        # for d in devices_list:
        #     if d.get('host') == new_device['host']:
        #         # return "Conflict, device already exists", 409
        #         # return jsonify(message="Conflict, device already exists", code=409) 
        #         return marshal_resp("Conflict, device already exists", 409, response_model)
                   
        # new_device['id'] = len(devices_list) + 1
        # devices_list.append(new_device)
        # # return "Device(s) added successfully", 201
        # # return jsonify(message="Device(s) added successfully", code=201)
        # return marshal_resp("Device(s) added successfully", 201, response_model)

        new_devices = api.payload['devices']
        print(new_devices)
        # for new_device in new_devices:
        #     print(new_device)
        #     for d in devices_list:
        #         if new_device['host'] == d.get('host'):
        #             return marshal_resp("Conflict, device already exists", 409, response_model)
        # new_device['id'] = len(devices_list) + 1
        # devices_list.append(new_device)
        # return marshal_resp("Device(s) added successfully", 201, response_model)
    
class DeleteDevice(Resource):
    """ Delete a device by its 'id' """
    
api.add_resource(Devices, '/devices', endpoint='Devices')

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.config['SWAGGER_UI_JSONEDITOR'] = True

    # app.config.from_pyfile('./config.py')
    app.run(host='0.0.0.0', port=8000, debug=True)
