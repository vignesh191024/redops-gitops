from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    service = data.get("service")
    status = data.get("status")
    
    # Dummy AI logic
    if status == "down":
        decision = f"Restart pod for {service}"
    else:
        decision = "No action needed"
    
    return jsonify({"decision": decision})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
