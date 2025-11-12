FROM python:3.11-slim

# (Optional) system deps if needed
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential git curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8501
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


