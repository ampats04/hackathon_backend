from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from database import engine
from sqlalchemy import text
from datetime import *
import json


events = Blueprint("events", __name__)
CORS(events)


@events.route("/create_event", methods=["GET", "POST"])
def create_event():

    if request.method == "POST":

        data = request.form

        if not data["name"]:
            response = jsonify({"messaage": "Event name is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["venue"]:
            response = jsonify({"messaage": "Event Venue is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["short_description"]:
            response = jsonify({"messaage": "Event Short Description is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["date"]:
            response = jsonify({"messaage": "Event Date is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["time"]:
            response = jsonify({"messaage": "Event Time is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif not data["max_volunteers"]:
            response = jsonify({"messaage": "Event Max Volunteers is required!"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        with engine.connect() as conn:

            query = text(
                "INSERT INTO events(name, venue, short_description, date, time, max_volunteers, datetime_created) VALUES(:name, :venue, :short_description, :date, :time, :max_volunteers, :datetimes)"
            )

            params = dict(
                name=data["name"],
                venue=data["venue"],
                short_description=data["short_description"],
                date=data["date"],
                time=data["time"],
                max_volunteers=data["max_volunteers"],
                datetimes=datetime.date,
            )

            conn.execute(query, params)

            conn.commit()

            response = jsonify(
                {"Success": True, "message": "Created events successfully"}
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


@events.route("/", methods=["GET", "OPTIONS"])
def getAllEvents():

    if request.method == "OPTIONS":
        response = jsonify({"Success": True, "message": "ughugh"})
        response.headers.add(
            "Access-Control-Allow-Headers", "ngrok-skip-browser-warning"
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    with engine.connect() as conn:

        allEvents = []
        query = text("SELECT * FROM events")

        result = conn.execute(query).fetchall()

        if not result:
            response = jsonify({"Success": False, "message": "No events at the moment"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        else:
            for row in result:
               
                allEvents.append(dict(row._mapping))

            response = jsonify(
                {
                    "success": True,
                    "message": "Events retrieved successfully",
                    "data": json.dumps(allEvents),
                }
            )

            response.headers.add("Access-Control-Allow-Origin", "*")

            return response


@events.route("/<id>", methods=["GET"])
def getEventbyId(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM  events WHERE id = :id")
        params = dict(id=id)

        result = conn.execute(query, params).fetchone()

        if result is None:
            response = jsonify({"Success": False, "message": "No events"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            response = jsonify({"Success": True, "message": "Events fetched"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


@events.route("<id>/update", methods=["PUT"])
def updateUser(id):

    data = request.form

    with engine.connect() as conn:
        query = text(
            "UPDATE users SET name = :name , venue = :venue, short_description = :short_description, date = :date, time = :time, max_volunteers = :max WHERE id = :id"
        )
        params = dict(
            id=id,
            name=data["name"],
            venue=data["venue"],
            short_description=data["short_description"],
            date=data["date"],
            time=data["time"],
            max_volunteers=data["max_volunteers"],
        )

        conn.execute(query, params)

        conn.commit()
        response = jsonify({"success": True, "message": "Updated events Successfully!"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


# DELETE


@events.route("<id>/delete", methods=["DELETE"])
def deleteUser(id):
    with engine.connect() as conn:

        query = text("DELETE FROM events WHERE id = :id")
        params = dict(id=id)

        conn.execute(query, params)

        conn.commit()

        response = jsonify({"success": True, "message": "Deleted events Successfully!"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
