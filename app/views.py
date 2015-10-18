from flask import Flask, request
from app import app
from flask import jsonify
from app.tools.dbConnector import * 
from app.tools import dbConnector
import json

@app.route('/')
@app.route('/index')
def index():
    return "test"

@app.route('/lol')
def index1():
    return "LOL"

@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)

@app.route('/db/api/clear/', methods=['GET', 'POST'])
def clear():
	con = connect()
	tables = ['post', 'thread', 'forum', 'subscription', 'follower', 'user']
	dbConnector.execute(con,"SET global foreign_key_checks = 0;")
	for table in tables:
		dbConnector.execute(con,"TRUNCATE TABLE %s;" % table)
	dbConnector.execute(con,"SET global foreign_key_checks = 1;")
	con.close()
	print "azaza"
	return jsonify({"code" : STATUS_CODE['OK'], "response" : 'OK' })


