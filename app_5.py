from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, fields, reqparse, marshal, model
import json

# List of Devices
devices_list = [
    {
        "id": 1,
        "host": "cml-core-rtr01",
        "username": "admin", 
        "password": "admin", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "iosxe",
    },
    {
        "id": 2,
        "host": "cml-core-rtr02",
        "username": "admin", 
        "password": "admin", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "iosxr",
    },
    {
        "id": 3,
        "host": "cml-dist-sw01",
        "username": "admin", 
        "password": "admin!", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "nxos",
    },
    {
        "id": 4,
        "host": "cml-dist-sw02",
        "username": "admin", 
        "password": "admin!", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "nxos",
    }
]

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    version="1.0",
    title="Cisco Sandbox APIs",
    description="A simple Devices API",
    doc = '/docs'
)

device_model = api.model(
    "device", {
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

# device_resp_model = api.model(
#     "dev", {
#         'id': fields.Integer(required=True, description='id'),
#         "host": fields.String(required=True, description='HostName/IP', default='cml-core01.example.com'),
#         'username': fields.String(required=True, description='username', default='admin'),
#         'password': fields.String(required=True, description='password', default='mYsEcrEt'),
#         'protocol': fields.String(required=True, description='protocol', default='ssh'),
#         'port': fields.Integer(required=True, description='port', default=22),
#         'os_type': fields.String(required=True, description='os_type', default='iosxe'),
#     },
# )


device_resp_model = device_model.clone(
    'devices_response', {
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
        ), response_code
    )

class Devices(Resource):
    """Shows list of current devices in the database, 
    and lets you POST to add new device(s)"""

    # @api.marshal_with(device_resp_model, code=200, description="List of device")    
    @api.marshal_list_with(device_resp_model, code=200, description="List of device", envelope='devices')
    def get(self):
        """Get the current devices"""
        return devices_list

    # @api.marshal_with(response_model)
    # @api.expect(device_post_model, validate=True)
    # def post(self):
    #     """Add a new device"""
    #     new_devices = api.payload['devices']
    #     print(new_devices)
    #     for new_device in new_devices:
    #         print(new_device)
    #         for d in devices_list:
    #             if new_device['host'] == d.get('host'):
    #                 return marshal_resp("Conflict, device already exists", 409, response_model)
    #     new_device['id'] = len(devices_list) + 1
    #     devices_list.append(new_device)
    #     return marshal_resp("Device(s) added successfully", 201, response_model)

    @api.expect(device_post_model, validate=True)
    # @api.response(400, 'Invalid input')
    # @api.response(409, 'Conflict')
    # @api.doc(responses={400, 'Invalid input', 409, 'Conflict'})
    # @api.doc(responses={
    #     201: 'Device(s) added successfully',
    #     400: 'Invalid input',
    #     409: 'Conflict'
    # })
    @api.marshal_with(response_model, code=201)
    def post(self):
        """Add new devices"""
        new_devices = api.payload.get("devices", [])
        # new_devices = api.payload['device']
        # new_devices = api.payload
        print(new_devices)
        if not new_devices:
            return marshal_resp("No devices provided", 400, response_model)
        added_devices = []
        for new_device in new_devices:
            if not all(new_device.values()):
                return marshal_resp("Missing device information", 400, response_model)
            if any(new_device[key] in (None, "") for key in new_device):
                return marshal_resp("Invalid device information", 400, response_model)
            if  any(new_device['host'] == d.get('host') for d in devices_list):
                return marshal_resp(f"Conflict, {new_device['host']} already exists", 409, response_model)
            # if any(new_device[key] == d.get(key) for d in devices_list for key in ("host", "username", "password", "protocol", "port", "os_type")):
            #     return marshal_resp("Conflict, device already exists", 409, response_model)
            added_device = dict(new_device)
            added_device["id"] = len(devices_list) + 1
            devices_list.append(added_device)
            added_devices.append(added_device)
        # return marshal_resp({"message": "Device(s) added successfully", "devices": added_devices}, 201, response_model)
        return marshal_resp("Device(s) added successfully", 201, response_model)    

class DeleteDevice(Resource):
    """ Delete a device by its 'id' """
    pass
        
api.add_resource(Devices, '/devices', endpoint='Devices')

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.run(host='0.0.0.0', port=8000, debug=True)


# in the above code, swagger ui not showing th right code 400, 409 and 201, can you fix the code ? 