from flask import Flask, Blueprint
from flask_restx import Resource, Api, fields, reqparse, marshal, model
from devices import devices_dict
import json

app = Flask(__name__)
api_ver = 'v1'
blueprint = Blueprint('api', __name__, url_prefix=f'/api/{api_ver}')

# api = Flask(__name__)

api = Api(
    blueprint, 
    version = '1.0',
    title = 'Network Device Automation (NetDevAuto)',
    description = 'FLASK RESTX API APP FOR THE NETWORK DEVICE AUTOMATION',
    default = 'NetDevAuto APIs', 
    default_label = 'Swagger APIs for NetDevAuto',
    prefix = '/',
    doc = '/docs')

app.register_blueprint(blueprint)

# /api/v1/swagger.json
# http://127.0.0.1:8000/api/v1/docs

########################################################################################################################
# class ListData(fields.Raw):
#     '''
#     Field for marshalling lists of other fields.
#     See :ref:`list-field` for more information.
#     :param cls_or_instance: The field type the list will contain.
#     This is a modified version of fields.List Class in order to get 'data' as key envelope
#     '''
#     def __init__(self, cls_or_instance, **kwargs):
#         self.min_items = kwargs.pop('min_items', None)
#         self.max_items = kwargs.pop('max_items', None)
#         self.unique = kwargs.pop('unique', None)
#         super(ListData, self).__init__(**kwargs)
#         error_msg = 'The type of the list elements must be a subclass of fields.Raw'
#         if isinstance(cls_or_instance, type):
#             if not issubclass(cls_or_instance, fields.Raw):
#                 raise MarshallingError(error_msg)
#             self.container = cls_or_instance()
#         else:
#             if not isinstance(cls_or_instance, fields.Raw):
#                 raise MarshallingError(error_msg)
#             self.container = cls_or_instance
#     def format(self, value):

#         if isinstance(value, set):
#             value = list(value)

#         is_nested = isinstance(self.container, fields.Nested) or type(self.container) is fields.Raw

#         def is_attr(val):
#             return self.container.attribute and hasattr(val, self.container.attribute)

#         # Put 'data' as key before the list, and return the dict
#         return {'data': [
#             self.container.output(idx,
#                 val if (isinstance(val, dict) or is_attr(val)) and not is_nested else value)
#             for idx, val in enumerate(value)
#         ]}

#     def output(self, key, data, ordered=False, **kwargs):
#         value = fields.get_value(key if self.attribute is None else self.attribute, data)
#         if fields.is_indexable_but_not_string(value) and not isinstance(value, dict):
#             return self.format(value)

#         if value is None:
#             return self._v('default')
#         return [marshal(value, self.container.nested)]

    # def schema(self):
    #     schema = super(ListData, self).schema()
    #     schema.update(minItems=self._v('min_items'),
    #                   maxItems=self._v('max_items'),
    #                   uniqueItems=self._v('unique'))

    #     # work around to get the documentation as I want
    #     schema['type'] = 'object'
    #     schema['properties'] = {}
    #     schema['properties']['data'] = {}
    #     schema['properties']['data']['type'] = 'array'
    #     schema['properties']['data']['items'] = self.container.__schema__

    #     return schema

# https://stackoverflow.com/questions/58919366/flask-restplus-fields-nested-with-raw-dict-not-model

########################################################################################################################
# class DictItem(fields.Raw):
#     def output(self, key, obj, *args, **kwargs):
#         try:
#             dct = getattr(obj, self.attribute)
#         except AttributeError:
#             return {}
#         return dct or {}
# device_attributes = {
# 'username': fields.String(required=True, description='username', default='device username'),
# 'password': fields.String(required=True, description='password', default='device password'),
# 'protocol': fields.String(required=True, description='protocol', default='protocol name'),
# 'port': fields.Integer(required=True, description='port', default='port number'),
# 'os_type': fields.String(required=True, description='os_type', default='device OS type'),
# }

# device_model = api.model('Device', {
#                          'device': DictItem(attribute = device_attributes)
#                             }
#                           )

# device_model = api.model('Devices', {'device': fields.String('device')})

########################################################################################################################

# device_model = api.model(
#     "device",
#     {
#         'username': fields.String(required=True, description='username', default='device username'),
#         'password': fields.String(required=True, description='password', default='device password'),
#         'protocol': fields.String(required=True, description='protocol', default='ssh'),
#         'port': fields.Integer(required=True, description='port', default=22),
#         'os_type': fields.String(required=True, description='os_type', default='iosxe'),
#     },
# )

# @api.doc(
#     hide=True,
#     params={'device': {'properties': {'password': {'type': 'string', 'format': 'password'}}}}
# )

########################################################################################################################

# device_nested = api.model(
#     "device", {
#         "username": fields.String(default='username'),
#         "password": fields.String(default='password'),
#         "protocol": fields.String(default='ssh'),
#         "port": fields.Integer(default=22),
#         "os_type": fields.String(default='os_type'),
#     }
# )

# device_model = api.model(
#     "devices", {
#         "device": fields.List(fields.Nested(device_nested)),
#     }
# )

########################################################################################################################

device_nested = api.model(
    "device",
    {
        'username': fields.String(required=True, description='username', default='device username'),
        'password': fields.String(required=True, description='password', default='device password'),
        'protocol': fields.String(required=True, description='protocol', default='protocol name'),
        'port': fields.Integer(required=True, description='port', default=22),
        'os_type': fields.String(required=True, description='os_type', default='device OS type'),
    },
)

device_model = api.model(
    "Devices",
    {
        "device": fields.Nested(device_nested),
    },
)

########################################################################################################################

device_parser = reqparse.RequestParser(bundle_errors=True)
# device_parser.add_argument('devices', required=True, choices=tuple(devices_dict.keys()), help='List of Devices')
device_parser.add_argument("device", type=str, required=True, help='Enter the device hostname/IP')
device_parser.add_argument("username", type=str, required=True, help='Enter the device username')
device_parser.add_argument("password", type=str, required=True, help='Enter the device password') ## TODO: Hide password
device_parser.add_argument("protocol", type=str, required=True, help='Enter the protocol name')
device_parser.add_argument("port", type=int, required=True, help='Enter the port number')
device_parser.add_argument("os_type", type=str, required=True, help='Enter the device OS type e.g. iosxe, iosxr, nxos')

put_parser = reqparse.RequestParser(bundle_errors=True)
put_parser.add_argument("device", type=str, choices=tuple(devices_dict.keys()), required=True, help='Select the device to Edit')

delete_parser = reqparse.RequestParser(bundle_errors=True)
delete_parser.add_argument("device", type=str, choices=tuple(devices_dict.keys()), required=True, help='Select the device to delete')


class NetworkDevices(Resource):
    def get(self):
        ''' Returns the List of devices '''
        return devices_dict
    
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
            
            devices_dict.update(new_device)
            return f'{new_device}\n{device} has been added successfully.', 201
        else: 
            return {'HTTP ERROR': 400}
        
    @api.expect(device_parser, validate=True)
    def put(self):
        ''' Update the device information'''
        args = device_parser.parse_args()

    @api.expect(device_parser, validate=True)
    def patch(self):
        ''' Update the device information'''
        args = device_parser.parse_args()
        
    @api.expect(delete_parser, validate=True)
    def delete(self):
        ''' Delete a device '''
        args = delete_parser.parse_args()
        device = args['device']
        
        if device in devices_dict.keys():
            remove_device = devices_dict.pop(device, None)

            if remove_device != None:
                return f"{device} has been removed"
            else:
                return f"{device} was notremoved"
        
api.add_resource(NetworkDevices, '/devices')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)