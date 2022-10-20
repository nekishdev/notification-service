swagger_spec = {
    "swagger": "2.0",
    "info": {
        "title": "Auth service",
        "description": "API for auth service",
        "version": "0.0.1"
    },
    "host": "localhost:8086",
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
