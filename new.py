
def bubble_sort(arr):
    n = len(arr)
    # Проходимо по масиву n-1 разів
    for i in range(n-1):
        # Проходимо по масиву з кроком n-i-1, оскільки після кожної ітерації
        # найбільший елемент відсортовано та можна його ігнорувати в майбутньому
        for j in range(0, n-i-1):
            # Порівнюємо сусідні елементи
            if arr[j] > arr[j+1]:
                # Якщо перший елемент більше другого, міняємо їх місцями
                arr[j], arr[j+1] = arr[j+1], arr[j]

print("Conflit was fixed.Thank you in andvance!")

