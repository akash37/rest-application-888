from flask import Flask, request
from database import DBConnect
from queries import *
import json

# Flask constructor takes the name of
# current module (__name__) as argument
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/index', methods=['GET'])
def hello_world():
    return "Hello World"


'''
    Create routes for sports, events and selection
'''

@app.route('/create_sport', methods=['POST'])
def create_sport():
    payload = request.json
    try:
        cur = db_connection.cursor()
        sql, sql_tuple = get_create_sport_query(payload)
        cur.execute(sql, sql_tuple)
        db_connection.commit()
    except Exception as err:
        return {"error": err}

    return {"status": 200}


@app.route('/create_event', methods=['POST'])
def create_event():
    payload = request.json
    try:
        cur = db_connection.cursor()
        sql, sql_tuple = get_create_event_query(payload)
        cur.execute(sql, sql_tuple)
        db_connection.commit()
    except Exception as err:
        return {"error": err}

    return {"status": 200}


@app.route('/create_selection', methods=['POST'])
def create_selection():
    payload = request.json
    try:
        cur = db_connection.cursor()
        sql, sql_tuple = get_create_selection_query(payload)
        cur.execute(sql, sql_tuple)
        db_connection.commit()
    except Exception as err:
        return {"error": err}
    return {"status": 200}


# Search Query takes in filter parameters and returns relevant events or sports
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("term")
    payload = request.json
    try:
        cur = db_connection.cursor()
        sql = "select name from sport where active = true and name like '%" + query + "%'" \
            " union select name from event where active = true and name like '%" + query + "%';"

        cur.execute(sql)
        output_1 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        result_1 = json.dumps(output_1)
        # result_2 = None
        # result_3 = None
        # if payload["threshold"]:
        #     sql2 = "select sport_id, count(*) from event where active=true group by event_id having count(*) >= " \
        #            + str(payload["threshold"]) + ";"
        #     cur.execute(sql2)
        #     output_2 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        #     result_2 = json.dumps(output_2)
        #
        # if payload["scheduled_start"]:
        #     sql3 = "select name from event where scheduled_start > " + str(payload["scheduled_start"]) + ";"
        #     cur.execute(sql3)
        #     output_3 = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        #     result_3 = json.dumps(output_3)

    except Exception as err:
        return {"error": err}

    return result_1


@app.route('/update_sport', methods=['POST'])
def update_sport():
    payload = request.json
    try:
        cur = db_connection.cursor()
        sport_id = str(payload["sport_id"])
        sql = "update sport set name = '" + str(payload["name"]) + "', active="+str(payload["active"]) + \
              " where sport_id=" + sport_id + ";"
        cur.execute(sql)
        db_connection.commit()
    except Exception as err:
        return {"error": err}

    return {"status": 200}


# Updates the event and corresponding sports based on active and inactive status
@app.route('/update_event', methods=['POST'])
def update_event():
    payload = request.json
    try:
        cur = db_connection.cursor()
        event_id = str(payload["event_id"])
        sport_id = str(payload["sport_id"])
        sql = "update event set status = '" + str(payload["status"]) + "', active = " + \
              str(payload["active"]) + ", type='" + str(payload["type"]) + \
              "', scheduled_start='" + str(payload["scheduled_start"]) + \
              "', actual_start='" + str(payload["actual_start"]) + \
              "', name='" + str(payload["name"]) + \
              "' where event_id=" + event_id + ";"
        cur.execute(sql)
        if payload["active"]:
            sql_sport = "update sport set active = true where sport_id=" + sport_id + ";"
            cur.execute(sql_sport)
        else:
            sql_event = "select count(*) from  event where active=true and sport_id=" + sport_id + ";"
            cur.execute(sql_event)
            res = cur.fetchone()
            print(res)
            if res[0] >= 1:
                sql_sport = "update sport set active = true where sport_id=" + sport_id + ";"
                cur.execute(sql_sport)
            else:
                sql_sport = "update sport set active = false where sport_id=" + sport_id + ";"
                cur.execute(sql_sport)

        db_connection.commit()

    except Exception as err:
        return {"error": err}

    return {"status": 200}


# Update selection updates a particular selection and activate or deactivates the corresponding events and sports
@app.route('/update_selection', methods=['POST'])
def update_selection():
    payload = request.json
    try:
        cur = db_connection.cursor()
        event_id = str(payload["event_id"])
        selection_id = str(payload["selection_id"])
        sql = "update selection set price = " + str(payload["price"]) + ", active = " +\
              str(payload["active"]) + " where selection_id = " + selection_id + ";"
        cur.execute(sql)
        if payload["active"]:
            sql_event = "update event set active = true where event_id=" + event_id + ";"
            cur.execute(sql_event)
        else:
            sql_selection = "select count(*) from selection where active=true and event_id="+event_id + ";"
            cur.execute(sql_selection)
            res = cur.fetchone()
            print(res)
            if res[0] >= 1:
                sql_event = "update event set active = true where event_id=" + event_id + ";"
                cur.execute(sql_event)
            else:
                sql_event = "update event set active = false where event_id=" + event_id + ";"
                cur.execute(sql_event)

        # Check for sport and activate and deactivate accordingly
        select_sport_sql = "select sport_id from event where event_id=" + event_id + ";"
        cur.execute(select_sport_sql)
        sport_id = str(cur.fetchone()[0])
        sql_sport = "select count(*) from event where active=true and sport_id=" + sport_id + ";"
        cur.execute(sql_sport)
        sport_count = cur.fetchone()
        if sport_count[0] >= 1:
            sql_sport = "update sport set active=true where sport_id=" + sport_id + ";"
            cur.execute(sql_sport)
        else:
            sql_sport = "update sport set active=false where sport_id=" + sport_id + ";"
            cur.execute(sql_sport)
        db_connection.commit()
    except Exception as err:
        return {"error": err}

    return {"status": 200}


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    db_connection = DBConnect.get_connection_object()
    app.run(debug=True)
