from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Updated Kafka Bridge URL (correct cluster DNS name)
KAFKA_BRIDGE_URL = "http://redops-kafka-console-bridge-service.redops.svc.cluster.local:8080/topics/alerts-infra"

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json
    kafka_payload = {
        "records": [
            {"value": data}
        ]
    }
    headers = {
        "Content-Type": "application/vnd.kafka.json.v2+json"
    }
    try:
        response = requests.post(KAFKA_BRIDGE_URL, headers=headers, json=kafka_payload)
        return jsonify({
            "kafka_status": response.status_code,
            "bridge_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
