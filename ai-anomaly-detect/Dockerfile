# Use official Python slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy app source
COPY ai-analyze.py .

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port
EXPOSE 8090

# Run the app
CMD ["python", "ai-analyze.py"]
