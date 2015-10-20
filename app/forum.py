from app import app
from flask import jsonify, request
from constants import *
from app.tools import forum, post
from app.tools import dbConnector
import urlparse
from app.tools import helpers
import json


@app.route('/db/api/forum/create/', methods=['POST'])
def create_forum():

	con = dbConnector.connect();
	params = request.json;
	
	try:

		helpers.check_params(params, ["name", "short_name", "user"])
		response = forum.create(con, params["name"], params["short_name"], params["user"]);

	except Exception as e:
		con.close();
		return json.dumps({"code": 3, "response": (e.message)})
	
	con.close();
	return json.dumps({"code": 0, "response": response});


@app.route('/db/api/forum/details/', methods=['GET'])
def forum_details():
	con = dbConnector.connect();
	params = helpers.json_from_get(request)
	try:
		helpers.check_params(params, ["forum"])
		response = forum.details(con, params["forum"], helpers.related_exists(params))
	except Exception, e:
		con.close;
		return json.dumps({"code": 3, "response": (e.message)})
	con.close();
	return json.dumps({"code": 0, "response": response});

@app.route('/db/api/forum/listPosts/', methods=['GET'])
def forum_list_posts():
	con = dbConnector.connect()
	params = helpers.json_from_get(request)
	optional = helpers.get_optional_params(
		params,
		["since",
		"limit",
		"order"]
	)
	related = helpers.related_exists(params)
	try:
		helpers.check_params(params, ["forum"])
		response = post.posts_list(con, entity = "forum", params=optional, identifier=params["forum"], related=related)
	except Exception, e:
		con.close;
		return json.dumps({"code": 3, "response": (e.message)})
	con.close();
	return json.dumps({"code": 0, "response": response});
