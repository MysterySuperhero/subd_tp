from app import app
from flask import jsonify, request
from constants import *
from app.tools import forum
from app.tools import dbConnector
import urlparse
from app.tools import helpers
import json


@app.route('/db/api/thread/create/', methods=['GET', 'POST'])
def create_thread():

	con = dbConnector.connect();
	params = request.json;

	try:
		helpers.check_params(params, ["name", "short_name", "user"])

		response = forum.forum(con, name, short_name, user);

	except Exception as e:
		con.close();
		return json.dumps({"code": 3, "response": (e.message)})
	
	con.close();
	return json.dumps({"code": 0, "response": response});