from app.tools import dbConnector
from app.tools import user


def create(con, name, short_name, user):
	dbConnector.update_query(
		con,
		'INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)', (name, short_name, user)
	);

	# check result of update query:
	forum = dbConnector.select_query(
		con,
		'SELECT id, name, short_name, user FROM forum WHERE short_name = %s', (short_name,)
	)

	return forum_description(forum);


def details(con, short_name, related):
	forum = dbConnector.select_query(
		con, 'SELECT id, name, short_name, user FROM forum WHERE short_name = %s', (short_name,)
	)

	if len(forum) == 0:
		raise Exception("Forum " + short_name + " not found")

	forum = forum_description(forum)

	if "user" in related:
		forum["user"] = user.details(con, forum["user"])
	return forum


def forum_listUsers(con, forum_shortname, optional):
	query = "SELECT user.id, user.name, user.email FROM user " \
	        "WHERE user.email IN (SELECT DISTINCT user FROM post WHERE forum = \'" + str(forum_shortname) + "\')"
	if "since_id" in optional:
		query += " AND user.id >= " + str(optional["since_id"][0])
	if "order" in optional:
		query += " ORDER BY user.name " + str(optional["order"][0])
	if "limit" in optional:
		query += " LIMIT " + str(optional["limit"][0])

	try:
		posts = dbConnector.select_query(con, query, ())
	except Exception as e:
		print (e.message)

	response = []
	for post in posts:
		res = user.details(con, str(post[2]))
		response.append(res)

	return response


def forum_description(forum):
	forum = forum[0]
	response = {
		'id': forum[0],
		'name': forum[1],
		'short_name': forum[2],
		'user': forum[3]
	}

	return response
