def calculate_factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def calculate_discount(price):
    if price > 100:
        discount = price * 0.2
    else:
        discount = price * 0.1
    return price - discount


def calculate_triangle_area(base, height):
    return (base * height) / 2


def validate_email(email):
    if '@' not in email or '.' not in email[email.index('@'):]:
        return False
    if email.index('@') == 0 or email.index('@') == len(email) - 1:
        return False
    return True


def calculate_sum(numbers):
    return sum(numbers)

