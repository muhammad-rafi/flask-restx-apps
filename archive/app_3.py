from flask import Flask, Blueprint
from flask_restx import Resource, Api, fields, reqparse, marshal, model
from devices import devices_dict
import json

app = Flask(__name__)
api_ver = 'v1'
blueprint = Blueprint('api', __name__, url_prefix=f'/api/{api_ver}')

# DevicesList = []
# print(type(devices_dict))
# print(DevicesList.append(devices_dict))

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
devices = devices_dict

# device_model = api.model(
#     "device",
#     {
#         'id': fields.Integer(required=True),
#         'device_name': fields.String(required=True, description='device name', default='device name'),
#         'username': fields.String(required=True, description='username', default='device username'),
#         'password': fields.String(required=True, description='password', default='device password'),
#         'protocol': fields.String(required=True, description='protocol', default='protocol name'),
#         'port': fields.Integer(required=True, description='port', default=22),
#         'os_type': fields.String(required=True, description='os_type', default='device OS type'),
#     },
# )
# -------------
device_nested = api.model(
    "device",
    {
        'username': fields.String(required=True, description='username', default='device username'),
        'password': fields.String(required=True, description='password', default='device password'),
        'protocol': fields.String(required=True, description='protocol', default='protocol name'),
        'port': fields.Integer(required=True, description='port', default=22),
        'os_type': fields.String(required=True, description='os_type', default='iosxe'),
    },
)

device_model = api.model(
    "Devices",
    {
        "device": fields.Nested(device_nested),
    },
)

# -------------

# device_model = api.inherit("Devices", device_nested,
#     {
#         "device": fields.List(fields.Nested(device_nested)),
#     },
# )

# -------------

# device_nested = api.model('Device', {
#     'username': fields.String(required=True, description='Username'),
#     'password': fields.String(required=True, description='Password'),
#     'protocol': fields.String(required=True, description='Protocol'),
#     'port': fields.Integer(required=True, description='Port'),
#     'os_type': fields.String(required=True, description='Operating System Type')
# })

# device_model = api.model('Devices', {
#     'devices': fields.Raw(required=True, description='Dictionary of Devices')
#     # 'devices': fields.List(fields.Nested(device_nested), required=True, description='List of Devices')
# })

# ------------------

# class DictItem(fields.Raw):
#     def output(self, key, obj, *args, **kwargs):
#         try:
#             dct = getattr(obj, self.attribute)
#         except AttributeError:
#             return {}
#         return dct or {}

# device_model = api.model(
#     "Devices",
#     {
#         "id": fields.String(readOnly=True),
#         "devices": DictItem(attribute=devices),
#     },
# )

device_parser = reqparse.RequestParser(bundle_errors=True)
device_parser.add_argument("device", type=str, required=True, help='Enter the device hostname/IP')
device_parser.add_argument("username", type=str, required=True, help='Enter the device username')
device_parser.add_argument("password", type=str, required=True, help='Enter the device password') ## TODO: Hide password
device_parser.add_argument("protocol", type=str, required=True, help='Enter the protocol name')
device_parser.add_argument("port", type=int, required=True, help='Enter the port number')
device_parser.add_argument("os_type", type=str, required=True, help='Enter the device OS type e.g. iosxe, iosxr, nxos')

put_parser = reqparse.RequestParser(bundle_errors=True)
put_parser.add_argument("device", type=str, choices=tuple(devices.keys()), required=True, help='Select the device to Edit')
put_parser.add_argument("username", type=str, required=True, help='Enter the device username')
put_parser.add_argument("password", type=str, required=True, help='Enter the device password') ## TODO: Hide password
put_parser.add_argument("protocol", type=str, required=True, help='Enter the protocol name')
put_parser.add_argument("port", type=int, required=True, help='Enter the port number')
put_parser.add_argument("os_type", type=str, required=True, help='Enter the device OS type e.g. iosxe, iosxr, nxos')

delete_parser = reqparse.RequestParser(bundle_errors=True)
delete_parser.add_argument("device", type=str, choices=tuple(devices.keys()), required=True, help='Select the device to delete')


class Devices(Resource):
    # @api.marshal_with(device_nested, code=200, description="List devices", envelope='Devices')
    @api.marshal_with(device_model, code=200, description="List devices")
    def get(self):
        ''' Returns the List of devices '''
        # return devices
        return {'devices': devices}
    
class CreateDevice(Resource):

    @api.expect(device_parser, validate=True)
    @api.marshal_with(device_model, code=201, description="Add a new device")
    def post(self):
        ''' Add a new device '''
        
        args = device_parser.parse_args()
        device = args['device']
        username = args['username']
        password = args['password']
        protocol = args['protocol']
        port = args['port']
        os_type = args['os_type']
        
        if device: 
            new_device = {
                device: {
                        'username': username,
                        'password': password,
                        'protocol': protocol,
                        'port': port,
                        'os_type': os_type
                         }
                        }
            
            devices.update(new_device)
            # return new_device
            return {'devices': new_device}
            # return f'{new_device}\n{device} has been added successfully.', 201
        else: 
            return {'HTTP ERROR': 400}

class Device(Resource):

    @api.expect(device_parser, validate=True)
    def get(self, device_name):
        ''' Returns the List of devices '''
        
        args = device_parser.parse_args()
        if device_name in devices.keys():
            return devices['device_name']
    
    @api.expect(device_parser, validate=True)
    def put(self, device_name):
        ''' Update the device information'''
        args = device_parser.parse_args()

    @api.expect(device_parser, validate=True)
    def patch(self, device_name):
        ''' Update the device information'''
        args = device_parser.parse_args()
        
    @api.expect(delete_parser, validate=True)
    # def delete(self, device_name):
    def delete(self):
        ''' Delete a device '''
        args = delete_parser.parse_args()
        device = args['device']
        
        if device in devices.keys():
            remove_device = devices.pop(device, None)

            if remove_device != None:
                return f"{device} has been removed"
            else:
                return f"{device} was notremoved"
        
api.add_resource(Devices, '/devices', endpoint='Devices')
api.add_resource(CreateDevice, '/devices/device', endpoint='CreateDevice')
api.add_resource(Device, '/device', endpoint='Device')

# api.add_resource(Device, '/device/<string:device_name>', endpoint='Device')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
