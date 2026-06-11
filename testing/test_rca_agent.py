from agents.rca_agent import RCAAgent

agent = RCAAgent()

response = agent(
    query="SELECT email FROM customers",
    error="no such column: email",
    database_schema={
        "customers": [
            "id",
            "customer_name",
            "customer_email",
            "age"
        ]
    }
)

print("\nROOT CAUSE:\n")
print(response.root_cause)