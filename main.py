def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


def calculate_discount(price):
    if price > 100:
        discount = price * 0.2
        final_price = price - discount
    else:
        discount = price * 0.1
        final_price = price - discount
    return final_price


def calculate_triangle_area(base, height):
    area = (base * height) / 2
      return area


def validate_email(email):
    if '@' not in email:
        return False
    
    if '.' not in email[email.index('@'):]:
        return False
    
    if email.index('@') == 0 or email.index('@') == len(email) - 1:
        return False
    return True


def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    result = total
    return resul

