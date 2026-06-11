import os
import dspy

from dotenv import load_dotenv

load_dotenv()

lm = dspy.LM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

dspy.configure(lm=lm)