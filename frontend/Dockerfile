# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# FIX: Explicitly passing the extra index flag here directly to the pip process
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]