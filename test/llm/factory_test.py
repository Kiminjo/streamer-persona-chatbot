import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.models.factory import ModelFactory

llm = ModelFactory().create_model(llm_type="llama3")
openai_llm = ModelFactory().create_model(llm_type="openai",
                                         api_key=os.environ["OPENAI_API_KEY"])

print(llm)
print(openai_llm)
