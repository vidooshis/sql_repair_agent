# from core.validator import QueryValidator

# print(
#     QueryValidator.validate(
#         "SELECT customer_email FROM customers"
#     )
# )

# print(
#     QueryValidator.validate(
#         "DROP TABLE customers"
#     )
# )

# print(
#     QueryValidator.validate_confidence("1.0")
# )

# print(
#     QueryValidator.validate_confidence("0.4")
# )






# from core.validator import QueryValidator

# queries = [
#     "SELECT * FROM customers",
#     "DROP TABLE customers",
#     "UPDATE customers SET age=30"
# ]

# for q in queries:
#     print(QueryValidator.validate(q))



from core.validator import QueryValidator


print(
    QueryValidator.validate(
        "DROP TABLE customers"
    )
)