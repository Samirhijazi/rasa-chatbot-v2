import streamlit as st
import replicate
import os

class Llama:

    os.environ['REPLICATE_API_TOKEN'] = "r8_T9KG5NCROKMWJYynZdrS2HJiKnEKMFb34wBKJ"
    # Function for generating LLaMA2 response
    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    def generate_llama2_response(messages, prompt_input):
        string_dialogue = ""
        
        for dict_message in messages:
            if dict_message["role"] == "user":
                string_dialogue += f"User: {dict_message['content']}\n\n"
            elif dict_message["role"] == "assistant" and dict_message["content"] is not None and not dict_message["content"].startswith("full response: "):
                string_dialogue += f"Assistant: {dict_message['content']}\n\n"
        
        response = replicate.run(
            'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
            input={
                "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                "temperature": 0.1,
                "top_p": 0.9,
                "max_length": 512,
                "repetition_penalty": 1
            }
        )
        return response
        