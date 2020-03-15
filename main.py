from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import sqlite3
import mydb

# Configure Flask
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return "try something like 'http://127.0.0.1:5000/user_interests/2/1000'"


# Alternate style would be a class that encapsulates all the methods.


@app.route('/user_interests/<int:userid>/<int:maxrecs>', methods=['GET'])
def get_user_interests(userid, maxrecs):
    # Expects http://127.0.0.1:5000/user_interests?/2/1000 where the 2 is user id, 10 is record limit.
    # Userid of 0 means all users.
    c: sqlite3.Connection = mydb.open_db()
    cur = c.cursor()
    # The JSON serializer alphabetizes by key so force this to the first record location.
    ret = {
        '000_metadata': {'userid': userid, 'maxrecs': maxrecs,
                         'columns': ['uid', 'user_handle', 'interest_tag', 'date_followed'],
                         'key is': 'uid'}
    }
    # Yikes! No input error checking, highly hackable! THough there is some protection with Flask's
    # routing parser insisting on integer above.
    if userid == 0:
        for row in cur.execute('SELECT * FROM user_interests LIMIT ?',
                               [maxrecs]).fetchall():
            # row like (2, 1, '"mvc2"', '"2017-06-27 16:26:52"')
            ret[str(row[0])] = row
    else:
        for row in cur.execute('SELECT * FROM user_interests WHERE user_handle=? LIMIT ?',
                               [userid, maxrecs]).fetchall():
            # row like (2, 1, '"mvc2"', '"2017-06-27 16:26:52"')
            ret[str(row[0])] = row
    mydb.close_db(c)
    return ret


def post(self):
    parser.add_argument("name")
    parser.add_argument("age")
    parser.add_argument("spec")
    args = parser.parse_args()
    student_id = int(max(STUDENTS.keys())) + 1
    student_id = '%i' % student_id
    STUDENTS[student_id] = {
        "name": args["name"],
        "age": args["age"],
        "spec": args["spec"],
    }
    return STUDENTS[student_id], 201


if __name__ == "__main__":
    # Get database set up if not already set up.
    conn: sqlite3.Connection = mydb.init_mydb()
    mydb.load_csvs_to_db(conn)
    mydb.close_db(conn)
    conn = None

    app.run(debug=True, use_reloader=False)
