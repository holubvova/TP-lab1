def calculate_area(length, width):
    return length * width

def is_even(num):
    return num % 2 == 0


def calculate_average_grade(*grades):
    return sum(grades) / len(grades)


def calculate_product(x, y):
    return x * y



def find_duplicates(numbers):
    duplicates = set()
    seen = set()

    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)

    return list(duplicates)

