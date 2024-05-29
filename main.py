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
client = OpenAI(api_key=''
)

# latitude =  '-33.865143'
# longitude = '151.209900'

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
    ouput_file_path = Path(__file__).parent / "output.mp3"
    audio_file= open(ouput_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription


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
    #response.with_streaming_response.method("output.mp3")
    

def run_conversation():
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the weather like?"},
            {"role": "assistant", "content": 'AI will use the OpenWeather API call to execute a Python script to get the current weather conditions from the user. It will provide an answer to the user in natural language and not list the conditons. It will also name the city where the user is. When referring to units of measurement it should pronounce the full words (e.g. "meters per second")'}
        ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
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
        }
        messages.append(response_message) 
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                # longitude=function_args.get("longitude"),
                # latitude=function_args.get("latitude"),
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
        text_to_speech(second_response.choices[0].message.content)
        return "to speech"
        # function_response_content = json.loads(messages[-1]["content"])
        
        # final_message = create_dynamic_message(function_response_content)
        
        # return final_message
frames = record_on_sound()
save_wav('output.wav', frames)
# print("Give me one moment.")
# PlaySound.playsound()
print(run_conversation())

