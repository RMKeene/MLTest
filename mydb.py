import sqlite3


def init_mydb():
    # Get database set up if not already set up.
    conn = None
    try:
        conn = sqlite3.connect("keene.db")
        print(sqlite3.version)
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
            level TEXT NOT NULL UNIQUE,
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
        if conn:
            conn.close()
