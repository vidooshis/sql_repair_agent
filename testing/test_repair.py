from agents.repair_agent import RepairAgent

agent = RepairAgent()

response = agent(

    query="""
    SELECT email
    FROM customers
    """,

    root_cause="""
    Query references non-existent
    column email.
    customer_email exists.
    """,

    database_schema={
        "customers": [
            "id",
            "customer_name",
            "customer_email",
            "age"
        ]
    }
)

print(response.corrected_query)
print(response.confidence)