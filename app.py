from flask import Flask, request, jsonify
import math
import re  # Add the regex module for input validation

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n):
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    if is_armstrong(n):
        return f"{n} is an Armstrong number because {' + '.join(f'{d}^{len(str(n))}' for d in str(n))} = {n}"
    return f"{n} is a fascinating number with unique properties."

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Input validation: allow integers and floating-point numbers, including negative numbers
    if not number or not re.match(r"^[-+]?\d+(\.\d+)?$", number):
        return jsonify({
            "number": number if number else "null",
            "error": True
        }), 400
    
    try:
        number = float(number)  # Convert to float to handle both integer and float cases
    except ValueError:
        return jsonify({
            "number": number,
            "error": "Invalid number format"
        }), 400
    
    # Determine properties
    properties = []
    if is_armstrong(int(number)):  # Armstrong check requires an integer
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Build response
    response = {
        "number": number,
        "is_prime": is_prime(int(number)),
        "is_perfect": is_perfect(int(number)),
        "properties": properties,
        "digit_sum": digit_sum(int(number)),  # Digit sum requires an integer
        "fun_fact": get_fun_fact(int(number))  # Fun fact requires an integer
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
