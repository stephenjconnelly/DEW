
def tools():
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
                "type": "function",
                "function": {
                    "name": "flip_a_coin",
                    "description": "AI will use the OpenWeather API call to execute a Python script to flip a coin and generate either heads or tails. It will provide an answer to the user in natural language.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        },
                    },
                },
            }
        ]
    return tools