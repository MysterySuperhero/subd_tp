import simplejson as json

from app import app
from flask import request
from app.tools import user, post
from app.tools import dbConnector
from app.tools import helpers


@app.route('/db/api/user/create/', methods=['POST'])
def create_user():

	con = dbConnector.connect()
	params = request.json

	optional = helpers.get_optional_params(params, values=["isAnonymous"])

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
	return json.dumps({"code": 0, "response": userr})


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

@app.route('/db/api/user/follow/', methods=['POST'])
def user_follow():

	con = dbConnector.connect()
	params = request.json

	try:
		helpers.check_params(params, ["follower", "followee"])
		response = user.follow(con=con, follower_email=params["follower"], followee_email=params["followee"])
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})

	con.close()
	return json.dumps({"code": 0, "response": response})

@app.route('/db/api/user/unfollow/', methods=['POST'])
def user_unfollow():
	con = dbConnector.connect()
	params = request.json

	try:
		helpers.check_params(params, ["follower", "followee"])
		response = user.unfollow(con=con, follower_email=params["follower"], followee_email=params["followee"])
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})

	con.close()
	return json.dumps({"code": 0, "response": response})

@app.route('/db/api/user/updateProfile/', methods=['POST'])
def user_updateProfile():
	con = dbConnector.connect()
	params = request.json

	try:
		helpers.check_params(params, ["about", "user", "name"])
		response = user.updateProfile(con=con, about=params["about"], user=params["user"], name=params["name"])
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	con.close()
	return json.dumps({"code": 0, "response": response})


@app.route('/db/api/user/listFollowers/', methods=['GET'])
def user_listFollowers():

	con = dbConnector.connect()

	params = helpers.json_from_get(request)

	optional = helpers.get_optional_params(params, ["limit", "order", "since_id"])

	try:
		helpers.check_params(params, ["user"])
		response = user.listFollowers(con, params["user"], optional)
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	con.close()
	return json.dumps({"code": 0, "response": response})


@app.route('/db/api/user/listFollowing/', methods=['GET'])
def user_listFollowing():

	con = dbConnector.connect()

	params = helpers.json_from_get(request)

	optional = helpers.get_optional_params(params, ["limit", "order", "since_id"])

	try:
		helpers.check_params(params, ["user"])
		response = user.listFollowing(con, params["user"], optional)
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	con.close()
	return json.dumps({"code": 0, "response": response})


@app.route('/db/api/user/listPosts/', methods=['GET'])
def user_listPosts():

	con = dbConnector.connect()

	params = helpers.json_from_get(request)

	optional = helpers.get_optional_params(params, ["limit", "order", "since"])

	try:
		helpers.check_params(params, ["user"])
		response = post.posts_list(con=con, entity="user", params=optional, identifier=params["user"], related=[])
	except Exception as e:
		con.close()
		return json.dumps({"code": 1, "response": (e.message)})
	con.close()
	return json.dumps({"code": 0, "response": response})