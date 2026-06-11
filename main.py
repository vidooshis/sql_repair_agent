from core.executor import QueryExecutor
from core.schema import get_schema
from core.error_parser import parse_error
from core.validator import QueryValidator

from agents.rca_agent import RCAAgent
from agents.repair_agent import RepairAgent
from memory.memory_manager import (
    find_incident,
    save_incident
)

executor = QueryExecutor()

rca_agent = RCAAgent()

repair_agent = RepairAgent()


query = """
SELECT email
FROM customers
"""

result = executor.execute(query)

if result["success"]:

    print("Query succeeded")
    print(result["result"])

else:

    print("\nQuery Failed")

    print(result["error"])

parsed_error = parse_error(
    result["error"]
)

memory_hit = find_incident(
    parsed_error["type"],
    parsed_error["value"]
)

print("\nParsed Error")

print(parsed_error)

if memory_hit:

    print("\nMEMORY HIT")

    print(memory_hit)

    repaired_query = (
        memory_hit["corrected_query"]
    )

    retry_result = executor.execute(
        repaired_query
    )

    print("\nSUCCESS FROM MEMORY")

    print(retry_result["result"])

    exit()



database_schema = get_schema()

print("\nSchema")

print(database_schema)

rca_response = rca_agent(

    query=query,

    error=result["error"],

    database_schema=database_schema
)

print("\nRoot Cause")

print(rca_response.root_cause)

repair_response = repair_agent(

    query=query,

    root_cause=rca_response.root_cause,

    database_schema=database_schema
)

print("\nCorrected Query")

print(repair_response.corrected_query)

print("\nConfidence")

print(repair_response.confidence)

query_valid = QueryValidator.validate(
    repair_response.corrected_query
)

confidence_valid = (
    QueryValidator.validate_confidence(
        repair_response.confidence
    )
)

if not query_valid["valid"]:

    print(
        f"Validation failed: {query_valid['reason']}"
    )

    exit()

if not confidence_valid:

    print(
        "Confidence too low"
    )

    exit()

print("\nRetrying Query...\n")

retry_result = executor.execute(
    repair_response.corrected_query
)
if retry_result["success"]:
    save_incident(
        parsed_error["type"],
        parsed_error["value"],
        repair_response.corrected_query
    )
    print("SUCCESS")

    print(retry_result["result"])

else:

    print("Repair Failed")

    print(retry_result["error"])