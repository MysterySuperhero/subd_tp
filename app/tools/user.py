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

	print "__BEFORE___"
	print (str(user))
	#check insertion
	user = dbConnector.select_query(
		con,
		'SELECT id, email, about, isAnonymous, name, username FROM user WHERE email = %s',
                           (email, )
	)
	print "__AFTER___"
	print (str(user))
	# user = user_description(user)

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

def user_description(user):
	user = user[0]
	print "___USER___"
	print(str(user))
	response = {
		# 'about': user[2],
		# 'email': user[1],
		# 'id': user[0],
		# 'isAnonymous': bool(user[3]),
		# 'name': user[4],
		# 'username': user[5]
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
# def user_followers(con, email):
# 	followers = []
# 	followers = 
