import fastjsonschema
from pyramid.request import Request
from cornice import Service

from ..controllers import login as LoginController

register = Service(name='register', description='Register', path='/register')

register_post_validator = fastjsonschema.compile({
    'type' : 'object',
    'properties' : {
        'login' : {'type' : 'string', 'minLength': 4, 'maxLength': 10},
        'password' : {'type' : 'string'},
        'email' : {'type' : 'string', 'format' : 'idn-email'}
    },
    'required': ['login', 'password', 'email'],
    'additionalProperties': False
})

def validate_register_data(request, **kwargs):
    register_post_validator(request.json_body)
    #strength_check(request.json_body['password'])

@register.post(validators=validate_register_data, accept='application/json')
def register_post(request: Request):
    LoginController.register(request, request.json_body)