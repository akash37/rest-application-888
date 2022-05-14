from flask import Flask, request
from database import DBConnect
from queries import *

# Flask constructor takes the name of
# current module (__name__) as argument
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/index', methods=['GET'])
def hello_world():
    return "Hello World"


@app.route('/create_sport', methods=['POST'])
def create_sport():
    payload = request.json
    cur = db_connection.cursor()
    sql, sql_tuple = get_create_sport_query(payload)
    cur.execute(sql, sql_tuple)
    db_connection.commit()
    return {"status": 200}


@app.route('/create_event', methods=['POST'])
def create_event():
    payload = request.json
    cur = db_connection.cursor()
    sql, sql_tuple = get_create_event_query(payload)
    cur.execute(sql, sql_tuple)
    db_connection.commit()
    return {"status": 200}


@app.route('/create_selection', methods=['POST'])
def create_selection():
    payload = request.json
    cur = db_connection.cursor()
    sql, sql_tuple = get_create_selection_query(payload)
    cur.execute(sql, sql_tuple)
    db_connection.commit()
    return {"status": 200}


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    print(data)
    return data


@app.route('/update', methods=['PUT'])
def update_sport():
    return


@app.route('/update', methods=['PUT'])
def update_event():
    return


@app.route('/update', methods=['PUT'])
def update_selection():
    return


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    db_connection = DBConnect.get_connection_object()
    app.run(debug=True)
