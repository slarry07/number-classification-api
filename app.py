from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math

app = Flask(__name__)
CORS(app)  # Enable CORS

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum([i for i in range(1, n) if n % i == 0]) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d**power for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("text", "No fun fact found.")
    except:
        return "Could not fetch fun fact."
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number based on various properties."""
    number = request.args.get("number")

    # Input validation
    if not number or not number.lstrip("-").isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)

    # Determine properties
    properties = ["even" if number % 2 == 0 else "odd"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(number))),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
