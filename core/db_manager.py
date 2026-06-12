import sqlite3
import pandas as pd
import re
import os
import streamlit as st
DEFAULT_DB_PATH = "database/session.db"
os.makedirs("database", exist_ok=True)

def validate_identifier(name):

    return bool(
        re.match(
            r"^[A-Za-z_][A-Za-z0-9_]*$",
            name
        )
    )

def get_connection():

    db_path = st.session_state.get(
        "db_path",
        DEFAULT_DB_PATH
    )

    return sqlite3.connect(db_path)

def create_table(
    table_name,
    columns
):
    if not validate_identifier(
        table_name
    ):
        raise ValueError(
            "Invalid table name"
        )
    for column_name, _ in columns:

        if not validate_identifier(
            column_name
        ):
            raise ValueError(
                f"Invalid column name: {column_name}"
            )
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {table_name}"
    )
    
    column_definitions = ", ".join(
        [
            f"{name} {datatype}"
            for name, datatype in columns
        ]
    )
    
    query = f"""
    CREATE TABLE IF NOT EXISTS
    {table_name}
    (
        {column_definitions}
    )
    """

    print("\n========== SQL ==========")
    print(query)
    print("=========================\n")

    cursor.execute(query)

    conn.commit()

    conn.close()

def insert_row(
    table_name,
    row_data
):

    conn = get_connection()

    cursor = conn.cursor()

    columns = ", ".join(row_data.keys())

    placeholders = ", ".join(
        ["?"] * len(row_data)
    )

    query = f"""
    INSERT INTO {table_name}
    ({columns})
    VALUES
    ({placeholders})
    """

    cursor.execute(
        query,
        tuple(row_data.values())
    )

    conn.commit()

    conn.close()




def fetch_table(
    table_name
):

    conn = get_connection()

    df = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        conn
    )

    conn.close()

    return df