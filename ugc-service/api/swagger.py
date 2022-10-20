from settings import settings

swagger_spec = {
    "swagger": "2.0",
    "info": {
        "title": "UGC-API service",
        "description": "API for UGC",
        "version": "0.0.1"
    },
    "host": settings.SWAGGER_HOST,
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
