# translate.py

from flask import Flask, request, jsonify
import requests
import json
import uuid
import datetime

app = Flask(__name__)

# Kafka Bridge URL
KAFKA_BRIDGE_URL = "http://redops-kafka-console-bridge-service.redops.svc:8080/topics/alerts-infra"
HEADERS = {"Content-Type": "application/vnd.kafka.json.v2+json"}

# Alert translator
def translate_alert(alert):
    first_alert = alert.get("alerts", [{}])[0]
    pod_name = first_alert.get("labels", {}).get("pod", "")

    if not pod_name:
        print("⚠️ Warning: 'pod' label missing in alert!")

    return {
        "incident": first_alert.get("labels", {}).get("alertname", "Unknown"),
        "urgency": first_alert.get("labels", {}).get("severity", "low"),
        "description": first_alert.get("annotations", {}).get("summary", ""),
        "pod": pod_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "uuid": str(uuid.uuid4())
    }

@app.route("/translate", methods=["POST"])
def translate():
    try:
        alert = request.get_json(force=True)
        print("✅ Received alert:")
        print(json.dumps(alert, indent=2))

        translated = translate_alert(alert)

        kafka_payload = {
            "records": [
                {"value": translated}
            ]
        }

        print("📦 Translated payload to Kafka:")
        print(json.dumps(kafka_payload, indent=2))

        print(f"🛫 Sending to Kafka Bridge at {KAFKA_BRIDGE_URL}...")
        response = requests.post(KAFKA_BRIDGE_URL, headers=HEADERS, json=kafka_payload)

        if response.ok:
            print(f"✅ Kafka Bridge ACK: {response.status_code} - {response.text}")
        else:
            print(f"❌ Kafka Bridge Error: {response.status_code}")
            print(f"❌ Kafka response: {response.text}")
            print(f"🔁 Payload sent: {json.dumps(kafka_payload)}")

        return jsonify({
            "status": "sent",
            "kafka_status": response.status_code,
            "kafka_response": response.text
        }), 200 if response.ok else response.status_code

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
