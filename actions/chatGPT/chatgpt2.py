import requests
import json
import openai
import time

# Set your API key
api_key = "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"
openai.api_key = api_key



# Define the previous conversation (if any)
previous_conversation = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
    # {'role': 'user', 'content': 'I want to eat'}
    
]

def send_response(msg):
    start_time = time.time()
    previous_conversation.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=previous_conversation, 
        temperature=0.7,
        max_tokens=50,
        stream=True
    )


    collected_contents = ""

    # Iterate through the stream of events
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            content = delta['content']
            collected_contents += content  # Append the content to the string


    print(collected_contents)
    previous_conversation.append(
        {'role': 'assistant', 'content': collected_contents}
    )
    print(time.time()-start_time)
    print(previous_conversation)

def get_response(msg):
    while True:
        # msg = input()
        send_response(msg)
