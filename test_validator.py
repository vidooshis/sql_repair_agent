from core.validator import QueryValidator

print(
    QueryValidator.validate(
        "SELECT customer_email FROM customers"
    )
)

print(
    QueryValidator.validate(
        "DROP TABLE customers"
    )
)

print(
    QueryValidator.validate_confidence("1.0")
)

print(
    QueryValidator.validate_confidence("0.4")
)