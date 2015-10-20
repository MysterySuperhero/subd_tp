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