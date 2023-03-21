
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
    print(f"With threading done for {time.time() - start} seconds")
    # result was 1.02120041847229

def get_all_weathers_with_threads():
    start = time.time()
    for city in CITIES:
        Thread(target=get_weather_by_city, args=(city,)).start()
    while True:
        if active_count() == 1:
            break
    print(f"Done for {time.time() - start} seconds")
    # With threading done for 0.5335173606872559

def main():
    print("[+] Run get_all_weathers")
    get_all_weathers()
    print("[+] Run get_all_weathers_with_threads")
    get_all_weathers_with_threads()

if __name__=="__main__":
    main()

#[+] Run get_all_weathers
#With threading done for 1.4126338958740234 seconds
#[+] Run get_all_weathers_with_threads
#Done for 0.2989945411682129 seconds