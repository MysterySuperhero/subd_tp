from app import app
from flask import jsonify, request
from constants import *
from app.tools import user
from app.tools import dbConnector
import urlparse
from app.tools import helpers
import json


@app.route('/db/api/user/create/', methods=['POST'])
def create_user():

	con = dbConnector.connect()
	params = request.json

	optional = intersection(params, values=["isAnonymous"])

	try:
		helpers.check_params(params, ["username", "about", "name", "email"])
		userr = user.create(con, params["username"], params["about"], params["name"], params["email"], optional)
	except Exception as e:
		if e.message == "5":
			con.close();
			return json.dumps({"code": 5, "response": (e.message)})
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	con.close()
	return json.dumps({code: 0, "response": userr})


@app.route('/db/api/user/details/', methods=['GET'])
def user_details():

	con = dbConnector.connect()
	params = helpers.json_from_get(request)

	try:
		helpers.check_params(params, ["user"])
		userr = user.details(con, params["user"])
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	
	con.close()
	return json.dumps({"code": 0, "response": userr})

def intersection(request, values):
	optional = dict([(k, request[k]) for k in set(values) if k in request])
	return optional
