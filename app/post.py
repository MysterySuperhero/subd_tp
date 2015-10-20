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
        response = post.details(con, params["post"], related)
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": response})

@app.route("/db/api/post/list/", methods=["GET"])
def post_list():
    con = dbConnector.connect()
    content = helpers.json_from_get(request)
    try:
        identifier = content["forum"]
        entity = "forum"
    except KeyError:
        try:
            identifier = content["thread"]
            entity = "thread"
        except Exception as e:
            con.close()
            return json.dumps({"code": 1, "response": (e.message)})

    optional = helpers.get_optional_params(request=content, values=["limit", "order", "since"])
    try:
        p_list = post.posts_list(con=con,entity=entity, params=optional, identifier=identifier, related=[])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": p_list})
