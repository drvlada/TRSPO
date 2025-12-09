import os
import time
import concurrent.futures
import matplotlib.pyplot as plt

# Параметри задачі
MAX_N = 10_000_000          
CHUNK_SIZE = 50_000        


def collatz_steps(n: int) -> int:
    steps = 0
    while n != 1:
        if n & 1:         
            n = 3 * n + 1
        else:              
            n //= 2
        steps += 1
    return steps


def run_with_list(n: int, processes: int):
    numbers = range(1, n + 1)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
        results = list(executor.map(collatz_steps, numbers, chunksize=CHUNK_SIZE))
    elapsed = time.perf_counter() - start
    avg_steps = sum(results) / len(results)
    return elapsed, avg_steps


def run_streaming(n: int, processes: int):
    numbers = range(1, n + 1)
    start = time.perf_counter()
    total_steps, count = 0, 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
        for value in executor.map(collatz_steps, numbers, chunksize=CHUNK_SIZE):
            total_steps += value
            count += 1

    elapsed = time.perf_counter() - start
    avg_steps = total_steps / count
    return elapsed, avg_steps


def main():
    n = MAX_N

    max_procs = os.cpu_count() or 4
    process_counts = [p for p in [1, 2, 4, 8] if p <= max_procs]

    print(f"Обчислення кількості кроків Колатца для чисел 1..{n}")
    print(f"Доступних ядер: {max_procs}, розмір чанка: {CHUNK_SIZE}\n")

    list_times = []
    stream_times = []

    for p in process_counts:
        elapsed_list, avg_list = run_with_list(n, p)
        elapsed_stream, avg_stream = run_streaming(n, p)

        list_times.append(elapsed_list)
        stream_times.append(elapsed_stream)

        print(f"Процесів: {p}")
        print(f"  Список           : {elapsed_list:.2f} c (avg = {avg_list:.4f})")
        print(f"  Без синхронізації: {elapsed_stream:.2f} c (avg = {avg_stream:.4f})")
        print("-" * 50)

    plt.figure(figsize=(10, 6))
    plt.plot(process_counts, list_times, marker='o', label='Список')
    plt.plot(process_counts, stream_times, marker='o', label='Без синхронізації')
    plt.xlabel('Кількість процесів')
    plt.ylabel('Час виконання (секунди)')
    plt.title('Порівняння швидкодії реалізацій Колатца')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
