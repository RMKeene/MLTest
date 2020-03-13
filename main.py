from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import sqlite3
import mydb

# Configure Flask
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class StudentsList(Resource):
    def get(self):
        return STUDENTS

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


api.add_resource(StudentsList, '/students/')

if __name__ == "__main__":
    # Get database set up if not already set up.
    conn: sqlite3.Connection = mydb.init_mydb()
    mydb.load_csvs_to_db(conn)
    mydb.close_db(conn)
    conn = None

    app.run(debug=True, use_reloader=False)

