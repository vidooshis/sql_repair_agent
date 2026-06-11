import dspy

from core.llm import lm


class RepairSignature(dspy.Signature):
    """
    Repair failed SQL queries.

    Return:
    - corrected_query: corrected SQL query
    - confidence: decimal between 0 and 1
    """

    query = dspy.InputField()

    root_cause = dspy.InputField()

    database_schema = dspy.InputField()

    corrected_query = dspy.OutputField(
        desc="Corrected SQL query only"
    )

    confidence = dspy.OutputField(
        desc="Float confidence score between 0.0 and 1.0"
    )


class RepairAgent(dspy.Module):

    def __init__(self):

        super().__init__()

        self.predict = dspy.Predict(
            RepairSignature
        )

    def forward(
        self,
        query,
        root_cause,
        database_schema
    ):

        return self.predict(
            query=query,
            root_cause=root_cause,
            database_schema=database_schema
        )