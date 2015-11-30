import simplejson as json

from app import app
from flask import request
from app.tools import thread, post
from app.tools import dbConnector
from app.tools import helpers


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
def details_thread():

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

@app.route("/db/api/thread/vote/", methods=['POST'])
def vote_thread():

    con  = dbConnector.connect()
    params = request.json

    try:
        helpers.check_params(params, ["vote", "thread"])
        response = thread.vote(con=con, vote=params["vote"], thread=params["thread"])
    except Exception as e:
        con.close()
        return json.dumps({"code":1, "response":(e.message)})
    con.close()
    return json.dumps({"code":1, "response":response})


@app.route("/db/api/thread/update/", methods=['POST'])
def update_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["message", "slug", "thread"])
        response = thread.update(con=con, message=params["message"], slug=params["slug"], thread=params["thread"])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})

    return json.dumps({"code": 0, "response": response})

@app.route("/db/api/thread/subscribe/", methods=['POST'])
def subscribe_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["user", "thread"])
        response = thread.subscribe(con=con, user=params["user"], thread=params["thread"])
    except Exception, e:
        con.close()
        return json.dumps({"code": 1, "response":(e.message)})
    
    con.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/db/api/thread/unsubscribe/", methods=['POST'])
def unsubscribe_thread():
    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["user", "thread"])
        response = thread.unsubscribe(con=con, user=params["user"], thread=params["thread"])
    except Exception, e:
        con.close()
        return json.dumps({"code": 1, "response":(e.message)})
    
    con.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/db/api/thread/open/", methods=['POST'])
def open_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["thread"])
        response = thread.open_close(con, params["thread"], isClosed=0)
    except Exception as e:
        con.close()
        return ({"code": 1, "response": (e.message)})

    con.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/db/api/thread/close/", methods=['GET','POST'])
def close_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["thread"])
        response = thread.open_close(con, params["thread"], isClosed=1)
    except Exception as e:
        con.close()
        return ({"code": 1, "response": (e.message)})
        
    con.close()
    return json.dumps({"code": 0, "response": response})

@app.route("/db/api/thread/restore/", methods=['POST'])
def restore_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["thread"])
        response = thread.restore_remove(con, params["thread"], isDeleted=0)
    except Exception as e:
        con.close()
        return ({"code": 1, "response": (e.message)})

    con.close()
    return json.dumps({"code": 0, "response": response})

@app.route("/db/api/thread/remove/", methods=['GET','POST'])
def remove_thread():

    con = dbConnector.connect()

    params = request.json

    try:
        helpers.check_params(params, ["thread"])
        response = thread.restore_remove(con, params["thread"], isDeleted=1)
    except Exception as e:
        con.close()
        return ({"code": 1, "response": (e.message)})

    con.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/db/api/thread/listPosts/", methods=["GET"])
def list_posts():
    con = dbConnector.connect()
    params = helpers.json_from_get(request)
    entity = "thread"
    optional = helpers.get_optional_params(request=params, values=["limit", "order", "since", "sort"])
    try:
        helpers.check_params(params, ["thread"])
        response = post.posts_list(con=con, entity="thread", params=optional, identifier=params["thread"], related=[])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})
    con.close()
    return json.dumps({"code": 0, "response": response})


@app.route("/db/api/thread/list/", methods=["GET"])
def list_thread():

    con = dbConnector.connect()

    params = helpers.json_from_get(request)

    optional = helpers.get_optional_params(request=params, values=["since", "limit", "order"])

    try:
        response = thread.list(con=con, required=params, optional=optional, related=[])
    except Exception as e:
        con.close()
        return json.dumps({"code": 1, "response": (e.message)})

    con.close()
    return json.dumps({"code": 0, "response": response})

    return