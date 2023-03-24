
import requests
import time
from threading import Thread, active_count

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
    print(f"Start {index} thread. Sleep 20 sec")
    time.sleep(20)
    print(f"End {index} thread")

def foo_5_sec(index: int):
    print(f"Start {index} thread. Sleep 5 sec")
    time.sleep(5)
    print(f"End {index} thread")

def foo_3_sec(index: int):
    print(f"Start {index} thread. Sleep 3 sec")
    time.sleep(3)
    print(f"End {index} thread")

def example_2_helper(arr: list, i:int, index: int) -> int:
    if i == 0:
        arr[i] = Thread(target=foo_20_sec,args=(index,), name=f"Thread-{index}")
    elif i % 3 == 1:
        arr[i] = Thread(target=foo_5_sec,args=(index,), name=f"Thread-{index}")
    else:
        arr[i] = Thread(target=foo_3_sec,args=(index,), name=f"Thread-{index}")
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
                print(f"{arr[i]} is still running")
                time.sleep(1)



if __name__=="__main__":
    #example_1()
    example_2()

#################### Prints example 1 ####################
#[+] Run get_all_weathers
#Done for 1.4126338958740234 seconds
#[+] Run get_all_weathers_with_threads
#With threading done for 0.2989945411682129 seconds

#################### Prints example 2 ####################
#Start 0 thread. Sleep 20 sec
#Start 1 thread. Sleep 5 sec
#Start 2 thread. Sleep 3 sec
#<Thread(Thread-0, started 30752)> is still running
#<Thread(Thread-1, started 33632)> is still running
#<Thread(Thread-2, started 6408)> is still running
#<Thread(Thread-0, started 30752)> is still running
#End 2 thread
#<Thread(Thread-1, started 33632)> is still running
#End 1 thread
#Start 3 thread. Sleep 3 sec
#<Thread(Thread-0, started 30752)> is still running
#Start 4 thread. Sleep 5 sec
#<Thread(Thread-3, started 31668)> is still running
#<Thread(Thread-0, started 30752)> is still running
#End 3 thread
#<Thread(Thread-4, started 6560)> is still running
#Start 5 thread. Sleep 3 sec
#End 4 thread
#End 5 thread
#End 0 thread