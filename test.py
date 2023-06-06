def calculate_rectangle_area(length, width):
    area = length * width
    return area

def calculate_square_area(side):
    area = side * side
    return area


def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

def calculate_average_grade(grade1, grade2, grade3, grade4, grade5):
    total = grade1 + grade2 + grade3 + grade4 + grade5
    average = total / 5
    return average


def calculate_foo(x, y):
    res = x * y
    return res


def find_duplicate(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates
