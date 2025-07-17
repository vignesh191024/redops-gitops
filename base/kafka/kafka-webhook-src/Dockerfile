FROM registry.access.redhat.com/ubi9/python-39
WORKDIR /app
COPY kafka_webhook.py .
RUN pip install flask kafka-python
CMD ["python", "kafka_webhook.py"]
