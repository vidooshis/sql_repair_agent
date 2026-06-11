class QueryValidator:

    HIGH_RISK = [
        "DROP",
        "DELETE",
        "TRUNCATE"
    ]

    MEDIUM_RISK = [
        "UPDATE",
        "ALTER"
    ]

    LOW_RISK = [
        "INSERT"
    ]

    @staticmethod
    def validate(query):

        query_upper = query.strip().upper()

        for op in QueryValidator.HIGH_RISK:

            if op in query_upper:

                return {
                    "valid": False,
                    "requires_approval": True,
                    "risk_level": "HIGH",
                    "reason": f"{op} can permanently remove data"
                }

        for op in QueryValidator.MEDIUM_RISK:

            if op in query_upper:

                return {
                    "valid": False,
                    "requires_approval": True,
                    "risk_level": "MEDIUM",
                    "reason": f"{op} modifies schema or data"
                }

        for op in QueryValidator.LOW_RISK:

            if op in query_upper:

                return {
                    "valid": False,
                    "requires_approval": True,
                    "risk_level": "LOW",
                    "reason": f"{op} changes database state"
                }

        return {
            "valid": True,
            "requires_approval": False,
            "risk_level": "NONE",
            "reason": None
        }

    @staticmethod
    def validate_confidence(confidence):

        try:
            return float(confidence) >= 0.7
        except:
            return False