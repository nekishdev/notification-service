from typing import Any

from flask import Response, jsonify


def abort(status: int, message: str) -> Response:
    return jsonify({
        'success': False,
        'message': message
    }), status


def success(message: str, data_: Any = None) -> Response:
    if data_ is not None:
        return jsonify(
            success=True,
            message=message,
            data=data_
        )
    else:
        return jsonify(
            success=True,
            message=message,
        )
