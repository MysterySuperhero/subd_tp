from app import app
from flask import jsonify
from app.tools.dbConnector import *
from app.tools import dbConnector


@app.route('/')
@app.route('/index')
def index():
	return "IT'S WORKING"


@app.route('/lol')
def index1():
	return "LOL"


@app.route('/data')
def names():
	data = {
		"names": ["John", "Jacob", "Julie", "Jennifer"]}
	return jsonify(data)


@app.route('/db/api/clear/', methods=['GET', 'POST'])
def clear():
	con = connect()
	tables = ['post', 'thread', 'forum', 'subscription', 'follower', 'user']
	dbConnector.execute(con, "SET global foreign_key_checks = 0;")
	for table in tables:
		dbConnector.execute(con, "TRUNCATE TABLE %s;" % table)
	dbConnector.execute(con, "SET global foreign_key_checks = 1;")
	con.close()
	return jsonify({
		"code": STATUS_CODE['OK'],
		"response": 'OK'})


@app.route('/db/api/status/', methods=['GET'])
def status():
	con = connect()
	response = []
	tables = ['user', 'thread', 'forum', 'post']

	for table in tables:
		currCount = len(dbConnector.select_query(con, 'SELECT id FROM ' + table, ()))
		response.append(currCount)

	statusResponse = {
		'user': response[0],
		'thread': response[1],
		'forum': response[2],
		'post': response[3]
	}

	con.close()

	stat = statusResponse
	return jsonify({
		"code": STATUS_CODE['OK'],
		"response": stat})
