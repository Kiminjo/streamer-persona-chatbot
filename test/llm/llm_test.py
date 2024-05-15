import sys
import os
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

sys.path.append(str(Path(__file__).resolve().parents[2]))
os.chdir(str(Path(__file__).resolve().parents[2]))

from src.models.llm import PersonaLLM

# Llama3 test
llm_type = "openai"
# model_name = "heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF/ggml-model-Q4_K_M.gguf"
model_name = "gpt-3.5-turbo"
embedding_model_name = "text-embedding-3-small"

llm = PersonaLLM(llm_type=llm_type,
                 model_name=model_name,
                 embedding_model_name=embedding_model_name,
                 api_key=os.environ["OPENAI_API_KEY"],
                 db_path="vector_db/index.faiss")

llm.search(query="한국의 대통령이 누구야?")
print(llm.input_prompt)

answer = llm.generate(prompt="한국의 대통령이 누구야?")
print(answer)
