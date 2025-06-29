FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
VOLUME /app/db
CMD ["python", "-m", "src.bot"]