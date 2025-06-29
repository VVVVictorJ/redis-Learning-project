# backend/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install uv, a fast Python package installer
RUN pip install uv

# Copy all backend files
COPY . .

# Install dependencies using uv from pyproject.toml
# Using --system to install in the global python environment
RUN uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 