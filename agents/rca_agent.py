import dspy

# Import configuration so DSPy gets initialized
from core.llm import lm


class RCA(dspy.Signature):
    """
    Analyze SQL query failures and explain the root cause.
    """

    query = dspy.InputField()
    error = dspy.InputField()
    schema = dspy.InputField()

    root_cause = dspy.OutputField(
        desc="Detailed explanation of why the query failed"
    )


class RCAAgent(dspy.Module):

    def __init__(self):
        super().__init__()

        self.predict = dspy.Predict(RCA)

    def forward(self, query, error, schema):

        return self.predict(
            query=query,
            error=error,
            database_schema=schema
        )