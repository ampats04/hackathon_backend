from functools import wraps
from flask import jsonify, request
import jwt

def authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            response = {"message": "Not Authenticated"}
            return jsonify(response)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "No Tokens"})
        return func(*args, **kwargs)

    return wrapped()