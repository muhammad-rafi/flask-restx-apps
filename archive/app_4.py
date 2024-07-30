from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields

api_v1 = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    api_v1,
    version="1.0",
    title="Cisco Sandbox APIs",
    description="A simple Devices API",
    doc = '/docs'
)

# ns = api.namespace("Sandbox Devices APIs", description="REST API Operations")

devices= {
    "sandbox-iosxe-recomm-1.cisco.com": {
        "username": "developer", 
        "password": "C1sco12345", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "iosxe"
        },
    "sandbox-iosxr-1.cisco.com": {
        "username": "admin", 
        "password": "C1sco12345", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "iosxr"
        },
    "sandbox-nxos-1.cisco.com": {
        "username": "admin", 
        "password": "Admin_1234!", 
        "protocol": "ssh",
        "port": 22,
        "os_type": "nxos"
        }
      }

device_nested = api.model(
    "device", {
        "username": fields.String(default='username'),
        "password": fields.String(default='password'),
        "protocol": fields.String(default='ssh'),
        "port": fields.Integer(default=22),
        "os_type": fields.String(default='os_type'),
    }
)

device_model = api.model(
    "devices", {
        "device": fields.Nested(device_nested),
    }
)

# @ns.route("/devices")
class Devices(Resource):
    """Shows a list of current devices, and lets you POST to add new device(s)"""
    
    @api.marshal_with(device_model, code=200, description="List of device")
    def get(self):
        """Get the current devices"""
        return {"devices": devices}

    @api.expect(device_model, validate=True)
    def post(self):
        """Dummy Method"""
        return "Success", 200
    
api.add_resource(Devices, '/devices', endpoint='Devices')

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    # app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.config.from_pyfile('./config.py')
    app.run(host='0.0.0.0', port=8000, debug=True)
