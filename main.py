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


@app.route('/courses_vs_interests_scores/<int:maxrecs>', methods=['GET'])
def generate_courses_vs_interests_scores(maxrecs):
    # Expects http://127.0.0.1:5000/courses_vs_interests_scores/1000 where the 2 is user id, 10 is record limit.
    c: sqlite3.Connection = mydb.open_db()

    ret = []

    # get list of user ids
    cur = c.cursor()
    userids = []
    for row in cur.execute('SELECT DISTINCT user_handle FROM user_interests LIMIT ?',
                           [maxrecs]).fetchall():
        userids.append(row[0])

    for userid in userids:
        # get courses a user takes
        user_courses = {}
        for row in cur.execute('SELECT * FROM user_course_views WHERE user_handle = ?', [userid]).fetchall():
            # uid, user_handle, view_date, course_id, author_handle, level, view_time_seconds
            # We will ignore summing view_time_seconds for now.  Not the immediate issue at hand.
            user_courses[row[3]] = row
        # Get union of all course tags
        course_tags = {}
        for course in user_courses:
            for row in cur.execute('SELECT * FROM course_tags WHERE course_id = ?', [course]).fetchall():
                # uid, course_id, course_tags
                # Just build dict of unique tags.
                course_tags[row[2]] = row

        # get interests of a user.
        interest_tags = {}
        for row in cur.execute('SELECT * FROM user_interests WHERE user_handle = ?', [userid]).fetchall():
            # uid, user_handle, interest_tag, date_followed
            interest_tags[row[2]] = row
            pass

        # Now correlate.  Lets try counting common terms, simple string compare for now.
        common_tags = {}
        for user_interest in interest_tags:
            if user_interest in course_tags:
                common_tags[user_interest] = user_interest

        ret.append({'user_handle': userid,
                    'user_score': float(len(common_tags)) /
                                  (len(interest_tags) + len(course_tags) - len(common_tags) + 1.0) ,
                    'common_tags': [*common_tags],
                    'user_interest_count': len(interest_tags),
                    'course_tag_count': len(course_tags)})

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
