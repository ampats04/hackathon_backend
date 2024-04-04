from flask import jsonify, Blueprint, request
from sqlalchemy import text
from database import engine
from events.events import getEventbyId
from users.users import getUserById
from datetime import *


apply_events = Blueprint("apply_event", __name__)


@apply_events.route("<user_id>/<event_id>/apply/")
def apply_event(user_id, event_id):

    with engine.connect() as conn:

        query = text(
            "INSERT INTO register_event(user_id, event_id, datetime_created) VALUES (:user_id, event_id, :datetime)"
        )
        params = dict(user_id=user_id, event_id=event_id, datetime=datetime.datetime())

        conn.execute(query, params)

        conn.commit()

        response = jsonify({"message": "Applied Successfully!"})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response
