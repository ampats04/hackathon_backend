from flask import Blueprint, make_response, request, jsonify, session
from flask_cors import CORS, cross_origin
import jwt
from database import engine
from sqlalchemy import text
from datetime import datetime, timedelta


users = Blueprint("users", __name__)
CORS(users)


@users.route("/registration", methods=["GET", "POST"])
# @cross_origin(allow_headers=["Content-Type"])
def registration():

    if request.method == "POST":

        data = request.form
        documents = request.files

        if not data["first_name"]:
            response = jsonify({"messaage": "First name is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["last_name"]:
            response = jsonify({"messaage": "Last name is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["birthday"]:
            response = jsonify({"messaage": "Birthday is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["email"]:
            response = jsonify({"messaage": "Email is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["phone_number"]:
            response = jsonify({"messaage": "Phone Number is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["password"]:
            response = jsonify({"messaage": "Password is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not documents["documents_1"]:
            response = jsonify({"messaage": "Document is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        with engine.connect() as conn:

            query = text(
                "INSERT INTO users(first_name, last_name, birthday, email, phone_number, username, password, datetime_created) VALUES(:first_name, :last_name, :birthday, :email, :phone_number, :username, :password, now())"
            )

            params = dict(
                first_name=data["first_name"],
                last_name=data["last_name"],
                birthday=data["birthday"],
                email=data["email"],
                phone_number=data["phone_number"],
                username=data["username"],
                password=data["password"],
                # documents_1=documents["documents_1"],
                date_created=datetime.timestamp,
            )

            result = conn.execute(query, params)

            conn.commit()

            response = jsonify({"message": "Registration Successfuly!"})
            response.headers.add("Access-Control-Allow-Origin", "*")

            return response


@users.route("/login", methods=["GET", "POST"])
# @cross_origin
def login():

    if request.method == "POST":

        data = request.form

        with engine.connect() as conn:

            query = text("SELECT * FROM users WHERE username = :username")
            params = dict(username=data["username"])

            result = conn.execute(query, params).fetchone()
            rows = result
        if result is not None:

            if data["password"] != result[7]:
                response = jsonify({"Success": False, "message": "Incorrect Password!"})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

            else:
                session.clear()
                session["username"] = result[6]

                response = jsonify(
                    {
                        "Success": True,
                        "message": "login success",
                        "data": dict(rows._mapping),
                    }
                )
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

        else:
            response = jsonify({"Success": False, "message": "Bad Credentials"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


@users.route("/", methods=["GET"])
# @cross_origin
def getAllUsers():

    with engine.connect() as conn:

        allUsers = []

        query = text("SELECT * FROM users ")

        result = conn.execute(query).fetchall()

        if not result:
            return jsonify({"message": "No users"})
        else:

            for rows in result:
                allUsers.append(dict(rows._mapping))

                response = jsonify({"Success": True, "message": "Retrieved User", "data": allUsers})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response


@users.route("/<id>", methods=["GET"])
# @cross_origin
def getUserById(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM users WHERE id = :id")

        result = conn.execute(query).fetchone()

        if not result:
            response = jsonify({"Success": False, "message": "No Users"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            response = jsonify(
                {"Success": True, "message": "Retrieved user successfully"}
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


# PUT


@users.route("<id>/update", methods=["POST"])
# @cross_origin
def updateUser(id):

    data = request.form

    with engine.connect() as conn:
        query = text(
            "UPDATE users SET email = :email, phone_number = :phone_number,username = :username, password = :password WHERE id = :id"
        )
        params = dict(
            id=id,
            email=data["email"],
            phone_number=data["phone_number"],
            username=data["username"],
            password=data["password"],
        )

        conn.execute(query, params)

        conn.commit()

        response = jsonify({"Success": True, "message": "Updated user successfully"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


# DELETE
@users.route("<id>/delete")
def deleteUser(id):
    with engine.connect() as conn:

        query = text("DELETE FROM users WHERE id = :id")
        params = dict(id=id)

        conn.execute(query, params)

        conn.commit()

        response = jsonify({"Success": True, "message": "Deleted user successfully"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
