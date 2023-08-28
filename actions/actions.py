import json
import socket
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionLlama(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )-> List[Dict[Text, Any]]:
        try:
            # Create a socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("localhost", 8887))  # Connect to the server's IP and port
            
            message = tracker.latest_message.get('text')
            # Create a dictionary with both message and category
            data = {
                "message": message,
            }

            # Send the data as JSON to the server
            json_data = json.dumps(data)
            client_socket.send(json_data.encode("utf-8"))


            # Receive and print the response from the server
            response = client_socket.recv(1024).decode("utf-8")
            intent_name = "conversation"
            json_response = {
                "intent": intent_name,
                "gpt_response": response
            }
            
            dispatcher.utter_message(text=json.dumps(json_response))   

        except Exception as e:
            print("Error:", str(e))
        finally:
            client_socket.close()  # Close the socket
        return []


class ActionConfermation(Action):
    def name(self) -> Text:
        return "action_confirmation"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )-> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")
        if name == "pass" :
            return [SlotSet("name", None)]
        else:
            jsonARRAY = {
                "text" : f"ok you can tell me now {name}",
                "name" : name
            }
            json_response = json.dumps(jsonARRAY)
            dispatcher.utter_message(text=json_response)
            return [SlotSet("name", None)]

