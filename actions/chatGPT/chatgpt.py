import os
import openai
import requests
from threading import Lock

# Set OpenAI API key outside the method (if you haven't set it as an environment variable)
openai_api_key = os.getenv("OPENAI_API_KEY", "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")

# Create a lock to handle concurrent requests
# gpt3_lock = Lock()

class GPT3:
    @staticmethod
    async def gpt3(stext):
        # with gpt3_lock:
        # Make a request to the GPT-3.5 Turbo model
        url = 'https://api.openai.com/v1/chat/completions'  # Use the v1/chat/completions endpoint
        headers = {
            'Authorization': 'Bearer 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', #Bearer GPT_API_KEY
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'gpt-3.5-turbo',  # Specify the model parameter
            'messages': [
                {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user queries.'},
                {'role': 'user', 'content': stext}
            ],
            'max_tokens': 10,
            'temperature': 0,  # Set temperature to control randomness of output
            'n': 1
        }

        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        print(response_json)

        # Extract the assistant's response if 'choices' key is present, otherwise handle the error
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content']
        else:
            return "Oops! Something went wrong. Unable to generate a response."

    response_history = set()

    @staticmethod
    async def get_answer(text):
        # OpenAI API Key
        openai.api_key = os.getenv("OPENAI_API_KEY", "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")

        # Use OpenAI API to get the response for the given user text
        response = openai.ChatCompletion.create(
            engine="gpt-3.5-turbo",
            prompt=text,
            max_tokens=35,
            n=1,
            temperature=0.2,
        )

        # # Check if the response is already in the history, if yes, get a new response
        # while response in GPT3.response_history:
        #     response = openai.Completion.create(
        #         engine="gpt-3.5-turbo",
        #         prompt=text,
        #         max_tokens=35,
        #         n=1,
        #         temperature=0,
        #     ).choices[0].text

        # # Add the response to the history
        # GPT3.response_history.add(response)

        # # Return the response from OpenAI
        return response
