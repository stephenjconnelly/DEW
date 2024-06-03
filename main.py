from openai import OpenAI
from openweather import OpenWeather
import json
import requests
import math
import sys 
import random
import playsound as PlaySound
from pathlib import Path
from record import record_on_sound, save_wav

latitude = "43.4631"
longitude = "-5.0561"

# latitude =  '-33.865143'
# longitude = '151.209900'




def get_random_numer(min, max):
    print(min, max)
    if(min != None or max != None):
        return str(random.randrange(int(min), int(max)))
    else:
        return "Number could not be generated"

    
#
# Gets current weather conditions from OpenWeather API. 
#
def get_current_weather(unit):
    print(latitude)
    print(longitude)
    try:
        API_key = ''
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

def speech_to_text():
    ouput_file_path = Path(__file__).parent / "output.wav"
    audio_file= open(ouput_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription)
    return transcription.text
    # return transcription.get('text', [])


def text_to_speech(message):
    print(message)
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=message
    )
    print(response)
    print(speech_file_path)
    response.stream_to_file(speech_file_path)
    PlaySound.playsound(speech_file_path)
    

def run_conversation(message):
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
            {"role": "assistant", "content": 'Use the provided functions to answer questions.'}
        ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                # "description": "Get the current weather in a given location",
                "description": 'AI will use the OpenWeather API call to execute a Python script to get the current weather conditions from the user. It will provide an answer to the user in natural language and not list the conditons. It will also name the city where the user is. When referring to units of measurement it should pronounce the full words (e.g. "meters per second")',
                "parameters": {
                    "type": "object",
                    "properties": {
                        # 'longitude': {
                        #     'type': 'string',
                        #     'description': 'A longitude value.'
                        # },
                        # 'latitude': {
                        #     'type': 'string',
                        #     'description': 'A latitude value.'
                        # },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    # "required": ["location"],
                },
            },
            "type": "function",
            "function": {
                "name": "get_random_number",
                "description": "AI will use the OpenWeather API call to execute a Python script to generate a random number in a range. It will provide an answer to the user in natural language.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        'min': {
                            'type': 'string',
                            'description': 'The minimum number in a range specified by the user.'
                        },
                        'max': {
                            'type': 'string',
                            'description': 'The maximum number in a range specified by the user. ',
                        }
                    },
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto", 
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_random_number": get_random_numer
        }
        messages.append(response_message) 
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if(function_to_call == get_random_numer):
                function_response = function_to_call(
                    min = function_args.get('min'),
                    max = function_args.get('max')
                )
            elif(function_to_call == get_current_weather):
                function_response = function_to_call(
                    unit=function_args.get("unit"),
                )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,        
        )
        # text_to_speech(second_response.choices[0].message.content)   
# frames = record_on_sound()
# save_wav('output.wav', frames)
message = sys.argv[1]
# print("Give me one moment.")
# PlaySound.playsound()
# message = speech_to_text()
print(run_conversation(message))

