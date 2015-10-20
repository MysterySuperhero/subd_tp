from app import app
from flask import request
from constants import *
from app.tools import thread
from app.tools import dbConnector
import urlparse
from app.tools import helpers
import json


@app.route('/db/api/thread/create/', methods=['GET', 'POST'])
def create_thread():

	con = dbConnector.connect();
	params = request.json

	optional = helpers.get_optional_params(params, ["isDeleted"])

	try:
		helpers.check_params(params, ["forum", "title", "isClosed", "user", "date", "message", "slug"])

		response = thread.create(con, params["forum"], params["title"], params["isClosed"], params["user"], params["date"], params["message"], params["slug"], optional);

	except Exception as e:
		con.close();
		return json.dumps({"code": 3, "response": (e.message)})
	
	con.close();
	return json.dumps({"code": 0, "response": response});

@app.route("/db/api/thread/details/", methods=["GET"])
def details():

    con = dbConnector.connect()
    params = helpers.json_from_get(request)
    required_data = ["thread"]
    related = helpers.related_exists(params)

    if 'thread' in related:
        con.close()
        return json.dumps({"code": 3, "response": "error"})
    try:
        helpers.check_params(params, required_data)
        response = thread.details(con, params["thread"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": response})

# def get_optional_params(request, values):
# 	optional = dict([(k, request[k]) for k in set(values) if k in request])
# 	return optional