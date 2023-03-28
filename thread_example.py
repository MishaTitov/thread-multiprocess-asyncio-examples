
import requests
import time
from threading import Thread
from threading import active_count
from threading import Lock

API_KEY = 	"122062fb6e9defff7091be745f70d1df"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?"
CITIES = ("Tel Aviv", "Jerusalem", "Berlin", "Moscow", "Tokyo", "Ulan Ude", "Budapest", "New York")

def get_weather_by_city(city: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    result = requests.get(WEATHER_URL, params=params)
    weather = result.text
    with open(f"{city}_weather_result","w") as f:
        f.write(weather)

def get_all_weathers():
    start = time.time()
    for city in CITIES:
        get_weather_by_city(city)
    print(f"Done for {time.time() - start} seconds")

def get_all_weathers_with_threads():
    start = time.time()
    for city in CITIES:
        Thread(target=get_weather_by_city, args=(city,)).start()
    while True:
        if active_count() == 1:
            break
    print(f"With threading done for {time.time() - start} seconds")

def example_1():
    print("[+] Run get_all_weathers")
    get_all_weathers()
    print("[+] Run get_all_weathers_with_threads")
    get_all_weathers_with_threads()

#################### example 2 ####################

def foo_20_sec(index: int):
    print(f"[+] Start {index} thread. Sleep 20 sec")
    time.sleep(20)
    print(f"[+] End {index} thread.")

def foo_5_sec(index: int):
    print(f"[+] Start {index} thread. Sleep 5 sec")
    time.sleep(5)
    print(f"[+] End {index} thread.")

def foo_3_sec(index: int):
    print(f"[+] Start {index} thread. Sleep 3 sec")
    time.sleep(3)
    print(f"[+] End {index} thread.")

def example_2_helper(arr: list, i:int, index: int) -> int:
    if i == 0:
        arr[i] = Thread(target=foo_20_sec,args=(index+1,), name=f"Thread-{index+1}")
    elif i % 3 == 1:
        arr[i] = Thread(target=foo_5_sec,args=(index+1,), name=f"Thread-{index+1}")
    else:
        arr[i] = Thread(target=foo_3_sec,args=(index+1,), name=f"Thread-{index+1}")
    index += 1
    arr[i].start()
    return index

def example_2():
    arr = [None] * 3
    index = 0
    for i in range(3):
        index = example_2_helper(arr,i,index)
    while index < 6:
        for i in range(3):
            if arr[i] and not arr[i].is_alive():
                index = example_2_helper(arr,i,index)
            else:
                print(f"[+] {arr[i]} is still running")
                time.sleep(1)

#################### example 3 ####################

counter = 0
lock = Lock()

def increment():
    global counter
    with lock:
        counter += 1

def worker(ind: int):
    global counter
    print(f"[+] Thread num.{ind+1} start with counter = {counter}",end=". ")
    for i in range(10000):
        increment()
    print(f"Thread num.{ind+1} end with counter = {counter}")

def example_3():
    # Lock here ensure that only one thread access the variable at the same time
    threads = []
    for i in range(10):
        t = Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("[+] Counter value:", counter)



if __name__=="__main__":
    #example_1()
    example_2()
    #example_3()

#################### Prints example 1 ####################
#[+] Run get_all_weathers
#Done for 1.4126338958740234 seconds
#[+] Run get_all_weathers_with_threads
#With threading done for 0.2989945411682129 seconds

#################### Prints example 2 ####################
#[+] Start 1 thread. Sleep 20 sec
#[+] Start 2 thread. Sleep 5 sec
#[+] Start 3 thread. Sleep 3 sec
#[+] <Thread(Thread-1, started 20612)> is still running
#[+] <Thread(Thread-2, started 9696)> is still running
#[+] <Thread(Thread-3, started 35088)> is still running
#[+] End 3 thread.
#[+] <Thread(Thread-1, started 20612)> is still running
#[+] <Thread(Thread-2, started 9696)> is still running
#[+] End 2 thread.
#[+] Start 4 thread. Sleep 3 sec
#[+] <Thread(Thread-1, started 20612)> is still running
#[+] Start 5 thread. Sleep 5 sec
#[+] <Thread(Thread-4, started 35796)> is still running
#[+] <Thread(Thread-1, started 20612)> is still running
#[+] End 4 thread.
#[+] <Thread(Thread-5, started 20068)> is still running
#[+] Start 6 thread. Sleep 3 sec
#[+] End 5 thread.
#[+] End 6 thread.
#[+] End 1 thread.

#################### Prints example 3 ####################
#[+] Thread num.1 start with counter = 0. Thread num.1 end with counter = 10000
#[+] Thread num.2 start with counter = 10000. Thread num.2 end with counter = 20000
#[+] Thread num.3 start with counter = 20000. Thread num.3 end with counter = 30000
#[+] Thread num.4 start with counter = 30000. Thread num.4 end with counter = 40000
#[+] Thread num.5 start with counter = 40000. Thread num.5 end with counter = 50000
#[+] Thread num.6 start with counter = 50000. Thread num.6 end with counter = 60000
#[+] Thread num.7 start with counter = 60000. Thread num.7 end with counter = 70000
#[+] Thread num.8 start with counter = 70000. Thread num.8 end with counter = 80000
#[+] Thread num.9 start with counter = 80000. Thread num.9 end with counter = 90000
#[+] Thread num.10 start with counter = 90000. Thread num.10 end with counter = 100000
#[+] Counter value: 100000