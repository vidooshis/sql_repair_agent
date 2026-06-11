import re


def parse_error(error_message):

    if "no such column" in error_message:

        match = re.search(
            r"no such column: (.+)",
            error_message
        )

        return {
            "type": "missing_column",
            "value": match.group(1)
        }

    if "no such table" in error_message:

        match = re.search(
            r"no such table: (.+)",
            error_message
        )

        return {
            "type": "missing_table",
            "value": match.group(1)
        }

    return {
        "type": "unknown",
        "value": error_message
    }