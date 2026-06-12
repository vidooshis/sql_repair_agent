import json
import os

MEMORY_FILE = "memory/incidents.json"

def load_memory():
    
    if not os.path.exists(MEMORY_FILE):
        return []
    os.makedirs(
        os.path.dirname(MEMORY_FILE),
        exist_ok=True
    )
    try:

        with open(MEMORY_FILE, "r") as file:

            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except Exception:

        return []
    
def save_incident(
    error_type,
    error_value,
    corrected_query
):
    os.makedirs(
        os.path.dirname(MEMORY_FILE),
        exist_ok=True
    )

    existing = find_incident(
        error_type,
        error_value
    )

    if existing:
        return

    memory = load_memory()

    memory.append(
        {
            "error_type": error_type,
            "error_value": error_value,
            "corrected_query": corrected_query
        }
    )

    with open(
        MEMORY_FILE,
        "w"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )

def find_incident(
    error_type,
    error_value
):

    memory = load_memory()

    for incident in memory:

        if (
            incident["error_type"] == error_type
            and
            incident["error_value"] == error_value
        ):

            return incident

    return None