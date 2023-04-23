def quicksort(arr):
    # Перевіряємо, чи містить масив менше двох елементів
    if len(arr) < 2:
        return arr
    else:
        # Встановлюємо перший елемент як опорний елемент
        pivot = arr[0]
        # Знаходимо всі елементи менші за опорний
        less = [i for i in arr[1:] if i <= pivot]
        # Знаходимо всі елементи більші за опорний
        greater = [i for i in arr[1:] if i > pivot]
        # Рекурсивно сортуємо обидва списки
        return quicksort(less) + [pivot] + quicksort(greater)

