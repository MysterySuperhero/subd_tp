from app import app
from flask import request
from constants import *
from app.tools import post
from app.tools import dbConnector
import urlparse
from app.tools import helpers
import json

@app.route('/db/api/post/create/', methods=['GET', 'POST'])
def post_create():

	con = dbConnector.connect()
	
	params = request.json

	optional = helpers.get_optional_params(
		params,
		["parent",
		"isApproved",
		"isHighlighted",
		"isEdited",
		"isSpam",
		"isDeleted"]
	)

	try:
		helpers.check_params(
			params,
			["date",
			"thread",
			"message",
			"user",
			"forum"]
		)

		response = post.create(con, params["date"], params["thread"], params["message"], params["user"], params["forum"], optional)

	except Exception as e:
		con.close()
		return json.dumps({"code": 3, "response": (e.message)})

	con.close()
	return json.dumps({"code": 0, "response": response})

@app.route("/db/api/post/details/", methods=["GET"])
def post_details():
    con = dbConnector.connect()
    params = helpers.json_from_get(request)
    required_data = ["post"]
    related = helpers.related_exists(params)
    try:
        helpers.check_params(params, required_data)
        print "___PARAMS___"
        print params["post"]
        response = post.details(con, params["post"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": response})
