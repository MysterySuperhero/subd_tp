from app.tools import dbConnector
from app.tools import user

def create(con, name, short_name, user):

	dbConnector.update_query(
		con, 
		'INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)', (name, short_name, user)
	);

	#check result of update query:
	forum = dbConnector.select_query(
		con,
		'SELECT id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
	)

	return forum_description(forum);

def details(con, short_name, related):
	forum = dbConnector.select_query(
		con, 'SELECT id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
	)

	if len(forum) == 0:
		raise Exception("Forum " + short_name + " not found")

	forum = forum_description(forum)

	if "user" in related:
		forum["user"] = user.details(con, forum["user"])
	return forum

def forum_listUsers(con, forum_shortname, optional):
	print "______LAST MAFAKA_______"
	query = "SELECT user FROM post WHERE forum = \'" + str(forum_shortname) + "\' GROUP BY user" 
	print query

	try:
		posts = dbConnector.select_query(con, query, ())
	except Exception as e:
		print (e.message)

	print posts

	response = []
	for post in posts:
		print str(post)
		res = user.details(con, str(post[0]))
		print res
		response.append(res)
	# query = "SELECT about, email, id, isAnonymous, name, username FROM user"
	print response

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
