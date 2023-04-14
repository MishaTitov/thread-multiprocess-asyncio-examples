import time
from multiprocessing import Process
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed


def foo_1_sec():
    print("[+] Sleeping 1 second")
    time.sleep(1)
    print("[+] Done Sleeping")

def foo_n_seconds(seconds):
    print(f"[+] Sleeping {seconds} seconds")
    time.sleep(seconds)
    print("[+] Done Sleeping")

def foo_n_seconds_with_return(seconds):
    print(f"[+] Sleeping {seconds} seconds")
    time.sleep(seconds)
    return "[+] Done Sleeping"

def example_1():
    print("Run without multiprocessing")
    start = time.perf_counter()
    foo_1_sec()
    foo_1_sec()
    finish = time.perf_counter()
    print(f"Finished in {finish-start} seconds")

    print("Run with multiprocessing")
    start = time.perf_counter()
    p1 = Process(target=foo_1_sec,)
    p2 = Process(target=foo_1_sec,)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    finish = time.perf_counter()
    print(f"Finished in {finish-start} seconds")

def example_2():
    print("Run loop with multiprocessing")
    start = time.perf_counter()
    processes = []
    for _ in range(10):
        p = Process(target=foo_n_seconds,args=(1.5,),)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    finish = time.perf_counter()
    print(f"Finished in {finish-start} seconds")

def example_3():
    print("Run with Pool multiprocessing")
    start = time.perf_counter()
    with Pool() as pool:
        pool.map(foo_n_seconds, [1]*10)
        pool.close()
        pool.join()
    finish = time.perf_counter()
    print(f"Finished in {finish-start} seconds")

def example_4():
    print("Run with ProcessPoolExecutor multiprocessing")
    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        # Also can be done with executor.map, but it will return resluts
        results = [executor.map(foo_n_seconds_with_return,1) for _ in range(10)]

        for f in as_completed(results):
            print(f.result())
    finish = time.perf_counter()
    print(f"Finished in {finish-start} seconds")

if __name__=="__main__":
    example_4()
