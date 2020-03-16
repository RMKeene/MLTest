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
    # Expects http://127.0.0.1:5000/user_interests/2/1000 where the 2 is user id, 10 is record limit.
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


@app.route('/compare_user_interests_and_courses/<int:usr1>/<int:usr2>', methods=['GET'])
def compare_user_interests_and_courses(usr1, usr2):
    # Expects http://127.0.0.1:5000/compare_user_interests_and_courses/1/3 being 2 user handles.
    return compare_user_interests_and_courses_impl(usr1, usr2)


def fetch_course_tags(cur, user_courses):
    course_tags = {}
    for course in user_courses:
        for row in cur.execute('SELECT * FROM course_tags WHERE course_id = ?', [course]).fetchall():
            # uid, course_id, course_tags
            # Just build dict of unique tags.
            course_tags[row[2]] = row
    return course_tags


def fetch_interest_tags(cur, userid):
    interest_tags = {}
    for row in cur.execute('SELECT * FROM user_interests WHERE user_handle = ?', [userid]).fetchall():
        # uid, user_handle, interest_tag, date_followed
        interest_tags[row[2]] = row
        pass
    return interest_tags


def fetch_user_courses(cur, userid):
    user_courses = {}
    for row in cur.execute('SELECT * FROM user_course_views WHERE user_handle = ?', [userid]).fetchall():
        # uid, user_handle, view_date, course_id, author_handle, level, view_time_seconds
        # We will ignore summing view_time_seconds for now.  Not the immediate issue at hand.
        user_courses[row[3]] = row
    return user_courses


def compare_user_interests_and_courses_impl(usr1, usr2):
    c: sqlite3.Connection = mydb.open_db()

    ret = []

    # get list of user ids
    cur = c.cursor()

    user_courses1 = fetch_user_courses(cur, usr1)
    course_tags1 = fetch_course_tags(cur, user_courses1)
    interest_tags1 = fetch_interest_tags(cur, usr1)
    user_courses2 = fetch_user_courses(cur, usr2)
    course_tags2 = fetch_course_tags(cur, user_courses2)
    interest_tags2 = fetch_interest_tags(cur, usr2)

    # How common are their interests?
    common_tags = {}
    # Ugly order squared :-(.  Converting these to numeric interest keys would be faster.
    # Better yet convert to numerics then use numpy or TensorFlow to correlate in GPU if needed.
    for user_interest1 in interest_tags1:
        for user_interest2 in interest_tags2:
            if user_interest1 == user_interest2:
                common_tags[user_interest1] = user_interest1
    # So the count could be an absolute metric of commonality. Or as a ratio of total interests vs. common.

    ret.append({'user_handle1': usr1, 'user_handle2': usr2,
                'user_score': len(common_tags),
                'common_tags': [*common_tags]})

    mydb.close_db(c)

    ret = {"data": ret}
    return ret


if __name__ == "__main__":
    # Get database set up if not already set up.
    conn: sqlite3.Connection = mydb.init_mydb()
    mydb.load_csvs_to_db(conn)
    mydb.close_db(conn)
    conn = None

    app.run(debug=True, use_reloader=False)
