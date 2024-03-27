from flask import Flask, jsonify
import random

app = Flask(__name__)

window_size = 10
number_list = []

def generate_primes(n):
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def generate_fibonacci(n):
    fibonacci = [0, 1]
    a, b = 0, 1
    while len(fibonacci) < n:
        a, b = b, a + b
        fibonacci.append(b)
    return fibonacci

def generate_even(n):
    return [num for num in range(2, n + 1) if num % 2 == 0]

def generate_random(n):
    return [random.randint(1, 100) for _ in range(n)]

def calculate_average(nums):
    if len(nums) == 0:
        return 0
    return sum(nums) / len(nums)

def update_window(new_number):
    global number_list
    if len(number_list) >= window_size:
        number_list.pop(0)  
    number_list.append(new_number)

@app.route('/numbers/<string:number_type>')
def get_numbers(number_type):
    global number_list
    prev_state = number_list.copy()

    if number_type == 'p':
        new_numbers = generate_primes(100)
    elif number_type == 'f':
        new_numbers = generate_fibonacci(20)
    elif number_type == 'e':
        new_numbers = generate_even(100)
    elif number_type == 'r':
        new_numbers = generate_random(20)
    else:
        return jsonify({"error": "Invalid number type"}), 400

    for num in new_numbers:
        if num not in number_list:
            update_window(num)
    
    avg = calculate_average(number_list[-window_size:])
    
    curr_state = number_list.copy()
    
    response = {
        "windowPrevState": str(prev_state),
        "windowCurrState": str(curr_state),
        "numbers": str(curr_state),
        "avg": avg
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=9876)
