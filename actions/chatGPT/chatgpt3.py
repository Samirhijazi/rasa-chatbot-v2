#new

import json
import openai
import time
import socket

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key
# Define the previous conversation (if any)
previous_conversation = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}
]
def send_response(msg):
    start_time = time.time()
    previous_conversation.append({'role': 'user', 'content': msg})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=previous_conversation,
        temperature=0.1,
        max_tokens=60,
        stream=True
    )

    collected_contents = ""

    # Iterate through the stream of events
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            content = delta['content']
            collected_contents += content  # Append the content to the string

    previous_conversation.append(
        {'role': 'assistant', 'content': collected_contents}
    )
    
    print(f"Processing time: {time.time() - start_time:.2f} seconds")
    print("Previous conversation:", previous_conversation)
    return collected_contents



def specifique(user_input, categories):
    conversation = previous_conversation.copy()
    if categories:
        conversation.append({'role': 'user', 'content': f"I am interested in {categories}"})
        response = send_response(user_input)

        if conversation[-1]['role'] == 'user' and f'interested in {categories}' in conversation[-1]['content'].lower():
            response = f" currently i talking with you as {categories} .  "
            response += send_response(user_input)
    else:
        conversation.append({'role': 'user', 'content': user_input})
        response = send_response(user_input)

    return response




    # conversation = previous_conversation.copy()
    # conversation.append({'role': 'user', 'content': f"I am interested in {categories}"})
    # conversation.append({'role': 'user', 'content': user_input})
    
    
    # for category in categories:
    # response = send_response(user_input)
    
    # return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8887))
server_socket.listen()

print("Server is Active")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            print(f"data: {data}")
            if not data:
                print("Connection closed by client")
                break

            # print(f"Received data: {data}")
            
            received_data = json.loads(data)
            user_message = received_data["message"]
            category = received_data["category"]
            print(f"Received message: {user_message}")
            print(f"Received category: {category}")
            
            # Process the data and send the response
            response = specifique(user_message, category)

            # Send the response back to the client
            client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print (f"An error occurred: {e}")
            break
    
    client_socket.close()