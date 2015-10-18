from app import app
from flask import jsonify, request
from constants import *
from app.tools import forum
from app.tools import dbConnector


@app.route('/db/api/forum/create/', methods=['GET', 'POST'])
def create():

	con = dbConnector.connect();
	params = request.json;

	try:
		check_params(params, ["name", "short_name", "user"])

		response = forum.create_forum(con, name, short_name, user);

	except Exception as e:
		con.close();
		return jsonify({"code": 3, "response": (e.message)})

	return jsonify({"code": 0, "response": response});

def check_params(params, required_params):
	for required_param in required_params:
		if required_param not in params:
			raise Exception("missing " + required_param)
		if params[required_param] is not None:
			try:
				params[required_param] = params[required_param].encode('utf-8')
			except Exception:
				continue
		return

