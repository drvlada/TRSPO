import threading

# Обчислення факторіалу числа
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    print(f"Факторіал {n}! = {result}")

# Сума квадратів
def sum_of_squares(n):
    result = sum(i * i for i in range(1, n + 1))
    print(f"Сума квадратів від 1 до {n} = {result}")

t1 = threading.Thread(target=factorial, args=(6,))
t2 = threading.Thread(target=sum_of_squares, args=(10,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Обчислення завершено.")
