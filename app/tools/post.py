from app.tools import user, forum, thread
from app.tools import dbConnector
import unicodedata

def create(con, date, thread, message, user, forum, optional):

	try:
		query = "INSERT INTO post (message, user, forum, thread, date"
		values = "(%s, %s, %s, %s, %s"
		parameters = [message, user, forum, thread, date]

		for param in optional:
			query += ", " + param
			values += ", %s"
			parameters.append(optional[param])
	except Exception as e:
		print e.message
	query += ") VALUES " + values + ")"
	update_thread_posts = "UPDATE thread SET posts = posts + 1 WHERE id = %s"
	update_parent = "UPDATE post SET parent =  %s WHERE id = %s"
	with con:
		cursor = con.cursor()
		cursor.execute(update_thread_posts, (thread, ))
		cursor.execute(query, parameters )
		con.commit()
		post_id = cursor.lastrowid
		cursor.close()

	post = post_query(con, post_id)
	del post["dislikes"]
	del post["likes"]
	del post["parent"]
	del post["points"]
	return post

def details(con, details_id, related):
    post = post_query(con, details_id)
    if post is None:
        raise Exception("no post with id = " + details_id)

    if "user" in related:
        post["user"] = user.details(con,post["user"])
    if "forum" in related:
        post["forum"] = forum.details(con, post["forum"], [])
    if "thread" in related:
        post["thread"] = thread.details(con, post["thread"], [])

    return post

def posts_list(con, entity, params, identifier, related=[]):
    query = "SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, " \
            "parent, points, thread, user FROM post WHERE " + entity + " = " + '\'' + str(''.join(identifier)) + '\''
    
    parameters = tuple()
    if "since" in params:
        query += " AND date >= %s"
        parameters += tuple(params["since"])

    query += " ORDER BY date " + ''.join(params["order"])

    if "limit" in params:
        query += " LIMIT " + ''.join(params["limit"])

    parameters += tuple('')
    post_ids = dbConnector.select_query(con, query, parameters)

    post_list = []
    for post in post_ids:
        pf = {
                'date': str(post[0]),
                'dislikes': post[1],
                'forum': post[2],
                'id': post[3],
                'isApproved': bool(post[4]),
                'isDeleted': bool(post[5]),
                'isEdited': bool(post[6]),
                'isHighlighted': bool(post[7]),
                'isSpam': bool(post[8]),
                'likes': post[9],
                'message': post[10],
                'parent': post[11],
                'points': post[12],
                'thread': post[13],
                'user': post[14],
            }
        if "user" in related:
            pf["user"] = user.details(con,pf["user"])
        if "forum" in related:
            pf["forum"] = forum.details(con,short_name=pf["forum"], related=[])
        if "thread" in related:
            pf["thread"] = thread.details(con,id=pf["thread"], related=[])
        post_list.append(pf)
    return post_list


def post_query(con, id):
    post = dbConnector.select_query(
    	con,
    	'SELECT date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, points, thread, user FROM post WHERE id = %s ;', (id, )
    )

    if len(post) == 0:
        return None

    post = post_formated(post)
    return post


def post_formated(post):
    post = post[0]
    post_response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }
    return post_response