from flask import Flask, request
from kafka import KafkaProducer
import json, os

app = Flask(__name__)
broker = os.getenv("KAFKA_BROKER")
topic = os.getenv("KAFKA_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=broker,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json()
    producer.send(topic, data)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
