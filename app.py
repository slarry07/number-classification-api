from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Helper functions
def is_armstrong(n):
    if isinstance(n, float):
        return False  # Armstrong numbers are only defined for integers
    digits = [int(d) for d in str(abs(int(n)))]
    length = len(digits)
    return sum(d ** length for d in digits) == abs(int(n))

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
    
    # Build response
    response = {
        "number": number,
        "properties": properties,  # Only armstrong, odd, or even
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
