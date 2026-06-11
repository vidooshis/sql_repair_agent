class QueryValidator:

    ALLOWED_OPERATIONS = [
        "SELECT"
    ]

    BLOCKED_OPERATIONS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE"
    ]

    @staticmethod
    def validate_confidence(confidence):

        try:
            confidence = float(confidence)

            return confidence >= 0.7

        except:
            return False

    @staticmethod
    def validate(query):

        query = query.strip().upper()

        for operation in QueryValidator.BLOCKED_OPERATIONS:

            if operation in query:
                return {
                    "valid": False,
                    "reason": f"Blocked operation detected: {operation}"
                }

        if not query.startswith("SELECT"):
            return {
                "valid": False,
                "reason": "Only SELECT queries allowed"
            }

        return {
            "valid": True,
            "reason": None
        }