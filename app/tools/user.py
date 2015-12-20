from app.tools import dbConnector


def create(con, username, about, name, email, optional):
	isAnonymous = 0;
	if "isAnonymous" in optional:
		isAnonymous = optional["isAnonymous"]

	user = dbConnector.update_query(
		con,
		'INSERT INTO user (username, about, name, email, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
		(username, about, name, email, isAnonymous,)
	)

	if user == "Error":
		raise Exception("5")

	# check insertion
	user = dbConnector.select_query(
		con,
		'SELECT id, email, about, isAnonymous, name, username FROM user WHERE email = %s',
		(email,)
	)

	return user_description(user)


def details(con, email):
	user = dbConnector.select_query(
		con,
		'SELECT id, email, about, isAnonymous, name, username FROM user WHERE email = %s LIMIT 1', (email,)
	)

	if len(user) == 0:
		raise Exception("User not found")

	user = user_description(user)

	following = dbConnector.select_query(
		con,
		'SELECT followee FROM follower WHERE follower = %s', (email,)
	)

	user["following"] = to_list(following)

	followers = dbConnector.select_query(
		con,
		'SELECT follower FROM follower WHERE followee = %s', (email,)
	)

	user["followers"] = to_list(followers)

	subscriptions = dbConnector.select_query(
		con,
		'SELECT thread FROM subscription WHERE user = %s', (email,)
	)

	user["subscriptions"] = to_list(subscriptions)

	return user


def follow(con, follower_email, followee_email):
	query = "INSERT INTO follower (follower, followee) VALUES (\'" + str(follower_email) + "\', \'" + str(
		followee_email) + "\')"

	dbConnector.update_query(con, query, ())

	return details(con, follower_email)


def unfollow(con, follower_email, followee_email):
	query = "DELETE FROM follower WHERE follower = \'" + str(follower_email) + "\' AND " + "followee = \'" + str(
		followee_email) + "\'"

	dbConnector.update_query(con, query, ())

	return details(con, follower_email)


def updateProfile(con, about, user, name):
	query = "UPDATE user SET about = \'" + str(about) + "\', email = \'" + str(user) + "\', name = \'" + str(
		name) + "\' WHERE email = \'" + str(user) + "\'"
	try:
		dbConnector.update_query(con, query, ())
	except Exception as e:
		print (e.message)
	print details(con, user)
	return details(con, user)


def listFollowers(con, email, optional):
	query = "SELECT followee FROM follower WHERE follower = \'" + str(email[0]) + "\'"

	if 'since_id' in optional:
		query += " AND id >= " + optional['since_id'][0]

	if 'order' in optional:
		query += " ORDER BY followee " + "".join(optional["order"][0])

	if 'limit' in optional:
		query += " LIMIT " + "".join(optional["limit"][0])

	try:
		followers = dbConnector.select_query(con, query, ())[0]
	except Exception as e:
		print (e.message)

	response = []
	for follower in followers:
		response.append(details(con, str(follower)))

	return response


def listFollowing(con, email, optional):
	query = "SELECT follower FROM follower WHERE followee = \'" + str(email[0]) + "\'"

	if 'since_id' in optional:
		query += " AND id >= " + optional['since_id'][0]

	if 'order' in optional:
		query += " ORDER BY follower " + "".join(optional["order"][0])

	if 'limit' in optional:
		query += " LIMIT " + "".join(optional["limit"][0])

	try:
		followees = dbConnector.select_query(con, query, ())[0]
	except Exception as e:
		print (e.message)

	response = []
	for followee in followees:
		response.append(details(con, str(followee)))

	return response


def listPosts(con, email, optional):
	query = "SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, points, thread, user FROM post WHERE user = \'" + str(
		email[0]) + "\'"

	if 'since' in optional:
		query += " AND date >= " + "\'" + optional['since'][0] + "\'"

	if 'order' in optional:
		query += " ORDER BY date " + "".join(optional["order"][0])

	if 'limit' in optional:
		query += " LIMIT " + "".join(optional["limit"][0])

	try:
		posts = dbConnector.select_query(con, query, ())
	except Exception as e:
		print (e.message)

	if posts != ():
		posts = posts[0]
		posts = {
			'date': posts[0].strftime("%Y-%m-%d %H:%M:%S"),
			'dislikes': posts[1],
			'forum': posts[2],
			'id': posts[3],
			'isApproved': posts[4],
			'isDeleted': posts[5],
			'isEdited': posts[6],
			'isHighlighted': posts[7],
			'isSpam': posts[8],
			'likes': posts[9],
			'message': posts[10],
			'parent': posts[11],
			'points': posts[12],
			'thread': posts[13],
			'user': posts[14]
		}

	return posts


def user_description(user):
	user = user[0]
	response = {
		'about': user[2],
		'email': user[1],
		'id': user[0],
		'isAnonymous': bool(user[3]),
		'name': user[4],
		'username': user[5]
	}
	return response


def to_list(a):
	lst = []
	for i in a:
		lst.append(i[0])
	return lst
