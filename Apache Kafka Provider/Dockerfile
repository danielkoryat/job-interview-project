FROM python:3.11.7

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ .

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Run the application
CMD ["python", "kafka_provider.py"]
