import time
import multiprocessing

def square_number(n):
    time.sleep(0.001)
    return n * n

def serial_square_list(numbers):
    return [square_number(n) for n in numbers]

def parallel_square_list(numbers, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(square_number, numbers)
    return results

if __name__ == "__main__":
    large_list = list(range(10000))
    start_time_serial = time.time()
    serial_results = serial_square_list(large_list)
    end_time_serial = time.time()
    print(f'Serial squaring finished in: {end_time_serial - start_time_serial:.4f} seconds')

    num_processes = multiprocessing.cpu_count()
    print(f'\nStarting parallel squaring using {num_processes} processes...')
    start_time_parallel = time.time()
    parallel_results = parallel_square_list(large_list, num_processes)
    end_time_parallel = time.time()
    print(f'Parallel squaring finished in: {end_time_parallel - start_time_parallel:.4f} seconds')
