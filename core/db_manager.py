import sqlite3
import pandas as pd
import streamlit as st
DB_PATH = "database/session.db"
def get_connection():
    return sqlite3.connect(DB_PATH)
    # return sqlite3.connect(
    #     st.session_state.db_path
    # )


def get_connection():

    return sqlite3.connect(DB_PATH)

def create_table(
    table_name,
    columns
):

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