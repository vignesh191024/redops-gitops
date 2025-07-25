from kafka import KafkaConsumer
import json
import subprocess
import uuid
import tempfile
import os

TOPIC_NAME = "alerts-infra"
BOOTSTRAP_SERVERS = "redops-kafka-kafka-bootstrap.redops.svc:9092"
GROUP_ID = "alert-group"

print(f"🔁 Kafka Trigger is listening to topic '{TOPIC_NAME}' on '{BOOTSTRAP_SERVERS}'...")

# Initialize consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=GROUP_ID
)

for message in consumer:
    alert = message.value

    if not isinstance(alert, dict):
        print(f"⚠️ Received unexpected payload (not dict): {alert}")
        continue

    print(f"📩 Received alert:\n{json.dumps(alert, indent=2)}")

    # Extract pod name
    pod_name = alert.get("pod")
    if not pod_name:
        print("⛔ Alert missing 'pod' label — skipping...")
        continue

    print(f"📦 Pod to restart: {pod_name}")

    # Generate unique PipelineRun name
    unique_name = f"ai-automation-run-{uuid.uuid4().hex[:6]}"
    print(f"🚀 Triggering Tekton PipelineRun: {unique_name}")

    try:
        # Load and modify the PipelineRun template
        with open("/app/tekton-pipelinerun.yaml", "r") as f:
            pipelinerun_yaml = f.read()
            pipelinerun_yaml = pipelinerun_yaml.replace("ai-automation-run", unique_name)
            pipelinerun_yaml = pipelinerun_yaml.replace("pod-name-placeholder", pod_name)

        # Write to temp YAML file
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".yaml") as tmpfile:
            tmpfile.write(pipelinerun_yaml)
            tmpfile_path = tmpfile.name

        # Apply PipelineRun
        result = subprocess.run(["oc", "apply", "-f", tmpfile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if result.returncode == 0:
            print(f"✅ Successfully triggered PipelineRun: {unique_name}")
        else:
            print(f"❌ Failed to apply PipelineRun:\n{result.stderr}")

    except Exception as e:
        print(f"❌ Exception while triggering pipeline: {e}")
