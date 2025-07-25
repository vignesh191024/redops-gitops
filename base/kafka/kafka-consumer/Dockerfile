FROM python:3.11-slim

WORKDIR /app

COPY kafka_bridge_consumer.py .

RUN pip install flask requests

EXPOSE 5000

CMD ["python", "-u","kafka_bridge_consumer.py"]
