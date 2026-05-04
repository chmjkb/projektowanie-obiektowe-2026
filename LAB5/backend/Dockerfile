FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir "fastapi>=0.115.0" "uvicorn[standard]>=0.32.0" "pydantic>=2.9.0"

COPY main.py ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
