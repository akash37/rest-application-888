from slugify import slugify

'''
    Create Queries for sport, event and selection
'''


def get_create_sport_query(data):
    slug = slugify(data["name"])
    sql = "insert into sport values (default, %s, %s, %s);"
    sql_tuple = (data["name"], slug, data["active"])
    return sql, sql_tuple


def get_create_event_query(data):
    slug = slugify(data["name"])
    sql = "insert into event values (default, %s, %s, %s, %s, %s, %s, %s, %s);"
    sql_tuple = (data["name"], slug, data["active"], data["type"], data["sport_id"], data["status"],
                 data["scheduled_start"], data["actual_start"])
    return sql, sql_tuple


def get_create_selection_query(data):
    sql = "insert into selection values (default, %s, %s, %s, %s, %s);"
    sql_tuple = (data["name"], data["event_id"], data["price"], data["active"], data["outcome"])
    return sql, sql_tuple

