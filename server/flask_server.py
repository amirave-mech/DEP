from flask import Flask, jsonify, request
from flask_cors import CORS
from interpreter.src.Interpreter import Interpreter, Journal

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"}), 200

# Example POST request with JSON input
@app.route("/", methods=["POST"])
def receive_data():
    interpreter = Interpreter()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        result = interpreter.feedBlock(Journal(data))
        # Process the received data (Example)
        response_data = {"received": str(result.value)}
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
