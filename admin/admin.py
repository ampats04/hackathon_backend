from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, session
from flask_cors import CORS, cross_origin
import jwt
from database import engine
from sqlalchemy import text

admin = Blueprint("admin", __name__)
CORS(admin)


@admin.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        data = request.form

        with engine.connect() as conn:

            query = text("SELECT * FROM admin WHERE username = :admin_username")
            params = dict(admin_username=data["username"])

            result = conn.execute(query, params).fetchone()
            rows = result

        if result is not None:
            if data["password"] != result[2]:
                response = jsonify({"Success": False, "message": "Incorrect Password!"})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            else:
                session.clear()
                session["username"] = result[1]
                response = jsonify(
                    {
                        "Success": True,
                        "message": "Login success",
                        "data": dict(rows._mapping),
                    }
                )
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
        else:
            response = jsonify({"Success": False, "message": "Bad Credentials"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
