import sqlite3
import streamlit as st

def get_schema():
    db_path = st.session_state.get(
        "db_path")

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema = {}

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema[table_name] = [
            col[1]
            for col in columns
        ]

    conn.close()

    return schema