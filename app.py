from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Helper functions
def is_prime(n):
    if n < 2 or not n.is_integer():  # Prime numbers are positive integers >= 2
        return False
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2 or not n.is_integer():  # Perfect numbers are positive integers >= 2
        return False
    n = int(n)
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    if not n.is_integer():  # Armstrong numbers are only for integers
        return False
    n = int(n)
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(d) for d in str(abs(int(n))))

def get_fun_fact(n):
    if is_armstrong(n):
        return f"{int(n)} is an Armstrong number because {' + '.join(f'{d}^{len(str(abs(int(n))))}' for d in str(abs(int(n))))} = {int(n)}"
    return f"{n} is a fascinating number with unique properties."

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Input validation
    try:
        number = float(number)  # Convert input to float
    except (ValueError, TypeError):
        return jsonify({
            "number": number if number else "null",
            "error": True
        }), 400
    
    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Ensure boolean output for is_prime and is_perfect
    is_prime_value = is_prime(number)
    is_perfect_value = is_perfect(number)

    # Build response
    response = {
        "number": number,
        "is_prime": is_prime_value,   # Always boolean
        "is_perfect": is_perfect_value,  # Always boolean
        "properties": properties,  # Only armstrong, odd, or even
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
