import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).resolve().parents[2]))
os.chdir(str(Path(__file__).resolve().parents[2]))

from src.models.vector_db import VectorDB

# Initialize the vector database
llm_type = "openai"
embedding_model_name = "text-embedding-3-small"
api_key = os.environ["OPENAI_API_KEY"]

vector_db = VectorDB(llm_type=llm_type,
                     embedding_model_name=embedding_model_name,
                     api_key=api_key)

# Initialize the dataset
documents = ["한국의 대통령은 윤석열입니다.",
             "미국의 대통령은 조 바이든입니다.",
             "일본의 대통령은 스가 요시히데입니다.",
             "중국의 대통령은 시진핑입니다.",
             "러시아의 대통령은 푸틴입니다."]

# Build the index
vector_db.build_index(docs=documents)

# Save the index
Path("vector_db").mkdir(exist_ok=True)
vector_db.save(db_path="vector_db/index.faiss")
