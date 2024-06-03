import requests
import math
import json
import random

latitude = "43.4631"
longitude = "-5.0561" 


def get_random_numer(min, max):
    print(min, max)
    if(min != None or max != None):
        return str(random.randrange(int(min), int(max)))
    else:
        return "Number could not be generated"

def flip_a_coin():
    # if(min != None or max != None):
    if(random.randrange(1, 2) == 1):
        return "Heads"
    else: 
        return "Tails"
    
    # else:
    
#
# Gets current weather conditions from OpenWeather API. 
#
def get_current_weather(unit):
    print(latitude)
    print(longitude)
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_key}'
        r = requests.get(url)        
        data = r.json()
        # print(data)
        main = data.get('main', [])
        weather = data.get('weather', [])
        wind = data.get('wind', [])
        rain = data.get('rain', [])
        city = data.get('name', [])
    except AttributeError as e:
        return "Error retrieving weather information. Please try again"
    # print(city)

    feelsLike = math.floor(main.get('feels_like', 0) - 273.15)
    temperature = math.floor(main.get('temp', 0) - 273.15)
    windSpeed = math.floor(wind.get('speed', 0))
    description = weather[0].get('description', "No description available") if weather else "No description available"
    precipitation = rain.get('1h', 0) if rain else "0"
    
    return json.dumps({
        #"city": city,
       # "name": name,
        "feelsLike": feelsLike,
        "temperature": temperature,
        "windSpeed": windSpeed,
        "description": description,
        "precipitation": precipitation,
        "city": city
    })
