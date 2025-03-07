import threading
import time


def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def thread_function(thread_id, barrier, start_value, end_value):
    start_time = time.perf_counter()
    primes = []
    for i in range(start_value, end_value + 1):
        print(f'Thread {thread_id} checking number {i}\n', end="")
        if is_prime(i):
            primes.append(i)
    total_time = time.perf_counter() - start_time

    print(f'Thread {thread_id} calling wait on barrier\n', end="")
    barrier.wait()  # Wait for all threads to complete the task before printing
    print(
        f'Thread {thread_id}: time = {total_time:.5f}: primes found = {len(primes)}\n', end="")


def main():

    # 4 is the number of threads to wait for
    barrier = threading.Barrier(4)

    # Create 4 threads, pass a "thread_id" and a barrier to each thread
    threads = []
    threads.append(threading.Thread(target=thread_function,
                                    args=(1, barrier, 1, 1000)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(2, barrier, 1000, 2000)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(3, barrier, 2000, 3000)))
    threads.append(threading.Thread(target=thread_function,
                                    args=(4, barrier, 3000, 4000)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()