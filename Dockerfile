FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy app source
COPY app.py .

# Expose Flask port
EXPOSE 5000


# Run Flask
CMD ["python", "app.py"]

