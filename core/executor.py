import sqlite3
import streamlit as st

class QueryExecutor:

    def __init__(self):
        self.db_path = (
            st.session_state["db_path"]
        )

    def execute(self, query):

        try:
            conn = sqlite3.connect(self.db_path)

            cursor = conn.cursor()

            cursor.execute(query)

            if cursor.description:
                rows = cursor.fetchall()

            else:
                conn.commit()
                rows = []

            conn.close()

            return {
                "success": True,
                "result": rows
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }