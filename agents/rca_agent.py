import dspy

from core.llm import lm


class RCA(dspy.Signature):
    """
    Analyze SQL query failures and explain the root cause.
    """

    query = dspy.InputField()

    error = dspy.InputField()

    database_schema = dspy.InputField()

    root_cause = dspy.OutputField(
        desc="Detailed explanation of why the query failed"
    )


class RCAAgent(dspy.Module):

    def __init__(self):

        super().__init__()

        self.predict = dspy.Predict(RCA)

    def forward(
        self,
        query,
        error,
        database_schema
    ):

        return self.predict(
            query=query,
            error=error,
            database_schema=database_schema
        )