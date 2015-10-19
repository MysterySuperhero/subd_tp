import MySQLdb as db
from constants import *


def connect():
    return db.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWORD,
                      db=DB_NAME,
                      charset=DB_CHARSET)


def update_query(con, query, params):
    try:
        cursor = con.cursor()
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        con.commit()
        cursor.close()
    except db.Error:
        con.rollback()
        cursor.close()
        return "Error"
    return inserted_id


def select_query(con, query, params):
    try:
        cursor = con.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
    except db.Error:
        cursor.close()
    return result


def select_query_dict(query,params):
    try:
        con = connect()
        cursor = con.cursor(db.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        con.close()
    except db.Error:
        raise db.Error("Database error in dict query")
    return result


def execute(connect, query):
    try:
        cursor = connect.cursor()
        cursor.execute(query)
        connect.commit()
        cursor.close()
    except db.Error:
        connect.rollback()
    cursor.close()
    return