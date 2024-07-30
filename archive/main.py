
from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, fields, reqparse, marshal, model


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# # App without Blueprint
# app = Flask(__name__)
# api = Api(
#     app, 
#     version = '1.0',
#     title = 'NetDevAuto',
#     description = 'FLASK RESTX API APP FOR THE NETWORK AUTOMATION',
#     prefix = '/',
#     doc = '/doc')

# # To define namespace instead of using default 
# ns = api.namespace('AppApi', description='Swagger APIs for Network Automation App')

# # To clear default namespace
# # api.namespaces = []
# # api.namespaces.pop(0)
# # api.namespaces.clear()

# @ns.route('/helloworld')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# App with Blueprint
app = Flask(__name__)
api_ver = 'v1'
blueprint = Blueprint('api', __name__, url_prefix=f'/api/{api_ver}')

api = Api(
    blueprint, 
    version = '1.0',
    title = 'NetDevAuto',
    description = 'FLASK RESTX API APP FOR THE NETWORK AUTOMATION',
    default = 'NetDevAuto APIs', 
    default_label = 'Swagger APIs for Network Automation App',
    prefix = '/',
    doc = '/doc')

app.register_blueprint(blueprint)

class HelloWorld(Resource):
    def get(self):
        return jsonify(hello='world')

api.add_resource(HelloWorld, '/helloworld')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
