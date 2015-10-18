from app.tools import dbConnector

def create_forum(con, name, short_name, user):
	update_query(con, 
		'INSERT INTO forum (name, short_name, user) VALUES (%s, %s, %s)', (name, short_name, user)
	);

	#check result of update query:
	forum = dbConnector.select_query(
		'SELECT id, name, short_name, user FROM forum WHERE short_name = %s', (short_name, )
	)

	return forum_description(forum);

def forum_description(forum):
    
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }

    return response