from app.tools import user, forum
from app.tools import dbConnector

def create(con, forum, title, isClosed, user, date, message, slug, optional):

    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    
    thread = dbConnector.update_query(con,'INSERT INTO thread (forum, title, isClosed, user, date, message, slug, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (forum, title, isClosed, user, date, message, slug, isDeleted, ))
    
    if thread == "Error":
        raise Exception("Thread already exists")

    thread = dbConnector.select_query(con,
            'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM thread WHERE slug = %s', (slug, )
        )
    thread = thread[0]
    response = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
    }
    return response

def details(con, id, related):

    thread = dbConnector.select_query(
        con,
        'SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM thread WHERE id = %s;', (id, )
    )

    if len(thread) == 0:
        raise Exception('Thread not founded')

    thread = thread[0]
    thread = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }

    if "user" in related:
        thread["user"] = user.details(con,thread["user"])
    if "forum" in related:
        thread["forum"] = forum.details(con=con,short_name=thread["forum"], related=[])

    return thread

def vote(con, vote, thread):
    if vote == -1:
        query = "UPDATE thread SET dislikes = dislikes + 1, points = points - 1 where id = " + str(thread)
    else:
        query = "UPDATE thread SET likes = likes + 1, points = points + 1 where id = " + str(thread)
    
    try:
        dbConnector.update_query(con, query, ())
    except Exception as e:
        print (e.message)

    return details(con, thread = id, related=[])


def update(con, message, slug, thread):
    query = "UPDATE thread SET slug = " + str(slug) + ", message = " + str(message) + " WHERE id = " + str(thread);
    try:
        dbConnector.update_query(con, query, ())
    except Exception as e:
        print(e.message)
    return details(con, thread = id, related=[])


def subscribe(con, user, thread):

    query = "INSERT INTO subscription (thread, user) VALUES (" + str(thread) + "," + str(user) + ")"

    try:
        dbConnector.update_query(con, update_query, ())
    except Exception as e:
        print (e.message)

    query = "SELECT thread, user FROM subscription WHERE thread = " + str(thread) + ", " + "user = " + str(user)

    try:
        sub = dbConnector.select_query(con, query, ()) 
    except Exception as e:
        print (e.message)

    result = {"thread": sub[0][0], "user": sub[0][1]}

    return result


# TODO: refactor exceptions raiser Exception(e.message) ???
def unsubscribe(con, user, thread):
    query = "DELETE FROM subscription WHERE thread = " + str(thread) + " AND user = " + str(user)

    try:
        dbConnector.update_query(con, query, ())
    except Exception as e:
        print (e.message) 

    result = {"thread": str(thread), "user": str(user)}
    return result

def open_close(con, thread, isClosed):
    query = "UPDATE thread SET isClosed = " + str(isClosed) + " WHERE id = " + str(thread);

    try:
        dbConnector.update_query(con, query, ())
    except Exception as e:
        print (e.message)

    response = {"thread": thread}

    return response

def restore_remove(con, thread, isDeleted):
    print "___ATTENTION___"

    posts = 0
    if isDeleted == 0:
        query = "SELECT COUNT(id) FROM post WHERE thread = " + str(thread)
        print query
        posts = dbConnector.select_query(con, query, ())[0][0]
    print posts

    query_thread = "UPDATE thread SET isDeleted = " + str(isDeleted) + ", posts = " + str(posts) + " WHERE id = " + str(thread)
    query_post = "UPDATE post SET isDeleted = " + str(isDeleted) + " WHERE thread = " + str(thread)

    print query_thread
    print query_post
    try:
        dbConnector.update_query(con, query_thread, ())
        dbConnector.update_query(con, query_post, ())
    except Exception as e:
        print (e.message)

    response = {"thread": thread }

    return response