from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Your Camel is so fat, he has three humps"}), 200

# Example POST request with JSON input
@app.route("/", methods=["POST"])
def receive_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Process the received data (Example)
        response_data = {"received": data, "message": "Data received successfully!"}
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
