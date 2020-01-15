import sqlite3


def create_table(db, query):
    """Creates a table (if not exists)"""

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
        except sqlite3.OperationalError:
            pass


def execute_command(db, query):
    """Execute a simple query which doesn't require any additional parameter"""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        res = cursor.execute(query)
        return res


def execute_command_with_params(db, query, params):
    """Execute a simple query which  requires additional parameter"""
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        res = cursor.execute(query, params)
        return res
