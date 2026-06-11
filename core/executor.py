import sqlite3


class QueryExecutor:

    def __init__(self, db_path="database/company.db"):
        self.db_path = db_path

    def execute(self, query):

        try:
            conn = sqlite3.connect(self.db_path)

            cursor = conn.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()

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