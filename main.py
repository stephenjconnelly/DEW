from openai import OpenAI
from openweather import OpenWeather
import json

import sys 
import random
import playsound as PlaySound
from pathlib import Path
from functions import flip_a_coin, get_current_weather, get_random_numer
from record import record_on_sound, save_wav
from tools import tools

latitude = "43.4631"
longitude = "-5.0561"

# latitude =  '-33.865143'
# longitude = '151.209900'





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
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools(),
        tool_choice="auto", 
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_random_number": get_random_numer,
            "flip_a_coin": flip_a_coin
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
            elif(function_to_call == flip_a_coin):
                function_response = function_to_call()
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
        return second_response.choices[0].message.content
        # text_to_speech(second_response.choices[0].message.content)   
# frames = record_on_sound()
# save_wav('output.wav', frames)
message = sys.argv[1]
# print("Give me one moment.")
# PlaySound.playsound()
# message = speech_to_text()
print(run_conversation(message))

