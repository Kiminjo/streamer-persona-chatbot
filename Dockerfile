# Set base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set working directory
WORKDIR /app

# Install dependencies using poetry 
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the rest of the files 
COPY . /app

# FastAPI 앱을 실행
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]