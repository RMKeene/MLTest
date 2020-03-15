import sqlite3
import csv

db_connection_string: str = "keene.db";

def init_mydb():
    # Get database set up if not already set up.
    conn = None
    try:
        conn: sqlite3.Connection = sqlite3.connect(db_connection_string)
        print('SQLite Version: ' + sqlite3.version)
        conn.execute("""CREATE TABLE IF NOT EXISTS 'course_tags' (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL,
            course_tags TEXT NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS 'user_assessment_scores' (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_handle TEXT NOT NULL,
            assessment_tag TEXT NOT NULL,
            user_assessment_date DATETIME NOT NULL,
            user_assessment_score INTEGER NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS 'user_course_views' (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_handle INTEGER NOT NULL,
            view_date DATE NOT NULL,
            course_id TEXT NOT NULL,
            author_handle INTEGER NOT NULL,
            -- Possible better implementation would be an integer enum value.
            level TEXT NOT NULL,
            view_time_seconds INTEGER NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS 'user_interests' (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_handle INTEGER NOT NULL,
            interest_tag TEXT NOT NULL,
            date_followed DATETIME NOT NULL
            )""")
    except sqlite3.Error as e:
        print(e)
    finally:
        # if conn:
        #   conn.close()
        #   conn = None
        pass
    return conn


def open_db() -> sqlite3.Connection:
    conn: sqlite3.Connection = sqlite3.connect(db_connection_string)
    return conn


def close_db(conn: sqlite3.Connection):
    if conn:
        conn.close()


def debug_table(conn, tablename):
    """ select * and print the first few lines of a table, to validate we have what we expect.
        in the table. """
    rowcount = 0
    cur = conn.cursor()
    for row in cur.execute(f'SELECT * FROM {tablename}').fetchall():
        rowcount += 1
        if rowcount > 5:
            break
        print(str(row))
    cur.close()


def load_csvs_to_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    for row in cur.execute('SELECT COUNT(*) FROM course_tags').fetchall():
        assert len(row) == 1
    if row[0] != 0:
        cur.close()
        print(f"Already loaded the csv files, skipping. (You can delete {db_connection_string} to force this to reload.)");
        return

    print("Loading course tags to DB.")
    cur = conn.cursor()
    rowcount = 0
    with open('data_files_ml_engineer/course_tags.csv', newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip = True
        for row in r:
            if skip:
                skip = False
                continue
            # print(', '.join(row))
            cur.execute('INSERT INTO course_tags(course_id, course_tags) VALUES (?, ?)', tuple(row))
            rowcount += 1
            # print(cur.lastrowid)
        conn.commit()
    cur.close()
    print(f"Loaded course_tags.csv, {rowcount} rows")
    debug_table(conn, 'course_tags')

    print("Loading user assessment scores to DB.")
    cur = conn.cursor()
    rowcount = 0
    with open('data_files_ml_engineer/user_assessment_scores.csv', newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip = True
        for row in r:
            if skip:
                skip = False
                continue
            # print(', '.join(row))
            cur.execute("""INSERT INTO 
                user_assessment_scores(user_handle, assessment_tag, user_assessment_date, user_assessment_score) 
                VALUES (?, ?, ?, ?)""", tuple(row))
            rowcount += 1
            # print(cur.lastrowid)
        conn.commit()
    cur.close()
    print(f"Loaded user_assessment_scores.csv, {rowcount} rows")
    debug_table(conn, 'user_assessment_scores')

    print("Loading user course views to DB.")
    cur = conn.cursor()
    rowcount = 0
    with open('data_files_ml_engineer/user_course_views.csv', newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip = True
        for row in r:
            if skip:
                skip = False
                continue
            # print(', '.join(row))
            cur.execute("""INSERT INTO 
                user_course_views(user_handle, view_date, course_id, author_handle, level, view_time_seconds) 
                VALUES (?, ?, ?, ?, ?, ?)""", tuple(row))
            rowcount += 1
            # print(cur.lastrowid)
        conn.commit()
    cur.close()
    print(f"Loaded user_course_views.csv, {rowcount} rows")
    debug_table(conn, 'user_course_views')

    print("Loading user interests to DB.")
    cur = conn.cursor()
    rowcount = 0
    with open('data_files_ml_engineer/user_interests.csv', newline='') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip = True
        for row in r:
            if skip:
                skip = False
                continue
            # print(', '.join(row))
            cur.execute("""INSERT INTO 
                user_interests(user_handle, interest_tag, date_followed) 
                VALUES (?, ?, ?)""", tuple(row))
            rowcount += 1
            # print(cur.lastrowid)
        conn.commit()
    cur.close()
    print(f"Loaded user_interests.csv, {rowcount} rows")
    debug_table(conn, 'user_interests')


