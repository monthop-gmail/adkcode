FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY adkcode/ /app/adkcode/

EXPOSE 8000
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
