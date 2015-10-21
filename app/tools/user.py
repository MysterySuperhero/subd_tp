from app.tools import dbConnector


def create(con, username, about, name, email, optional):
	isAnonymous = 0;
	if "isAnonymous" in optional:
		isAnonymous = optional["isAnonymous"]

	user = dbConnector.update_query(
		con, 
		'INSERT INTO user (username, about, name, email, isAnonymous) VALUES (%s, %s, %s, %s, %s)', (username, about, name, email, isAnonymous, )
	)

	if user == "Error":
		raise Exception("5")

	#check insertion
	user = dbConnector.select_query(
		con,
		'SELECT id, email, about, isAnonymous, name, username FROM user WHERE email = %s',
                           (email, )
	)

	return user_description(user)

def details(con, email):
	user = dbConnector.select_query(
		con,
		'SELECT id, email, about, isAnonymous, name, username FROM user WHERE email = %s LIMIT 1', (email, )
	)

	if len(user) == 0:
		raise Exception("User not found")

	user = user_description(user)

	following = dbConnector.select_query(
		con,
		'SELECT followee FROM follower WHERE follower = %s', (email, )
	)

	user["following"] = to_list(following)
		
	followers = dbConnector.select_query(
		con,
		'SELECT follower FROM follower WHERE followee = %s', (email, )
	)

	user["followers"] = to_list(followers)

	subscriptions = dbConnector.select_query(
		con,
		'SELECT thread FROM subscription WHERE user = %s', (email, )
	)

	user["subscriptions"] = to_list(subscriptions)

	return user

def follow(con, follower_email, followee_email):
	query = "INSERT INTO follower (follower, followee) VALUES (\'" + str(follower_email) + "\', \'" + str(followee_email) + "\')"

	dbConnector.update_query(con, query, ())

	return details(con, follower_email)

def unfollow(con, follower_email, followee_email):
	query = "DELETE FROM follower WHERE follower = \'" + str(follower_email) + "\' AND " + "followee = \'" + str(followee_email)  + "\'"

	dbConnector.update_query(con, query, ())

	return details(con, follower_email)

def updateProfile(con, about, user, name):
	query = "UPDATE user SET about = \'" + str(about) + "\', email = \'" + str(user) + "\', name = \'" + str(name) + "\' WHERE email = \'" + str(user) + "\'"
	try:
		dbConnector.update_query(con, query, ())
	except Exception as e:
		print (e.message)
	print details(con, user)
	return details(con, user)


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

