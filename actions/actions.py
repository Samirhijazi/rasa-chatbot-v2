from typing import Any, Text, Dict, List, Union
from datetime import datetime, timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionExecuted, Restarted, AllSlotsReset, FollowupAction
from rasa_sdk.forms import FormValidationAction
import re
import pickle
import random
import streamlit as st    
from actions.degree_model.bert_model import get_sentence_embedding
from actions.chatGPT.chatgpt import GPT3
from actions.Llama2_model.llama import Llama
from dotenv import load_dotenv
import json
import spacy

nlp1 = spacy.load(r".\actions\username_model\model-best")
    
class ActionQueryBot(Action):
    def name(self) -> Text:
        return "action_slots_values"
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        print(intent)
        print(tracker.get_slot("degree"))

        # Check if the required slots are filled
        if not tracker.get_slot("side"):
            dispatcher.utter_message(template="utter_ask_side")
            return [SlotSet("requested_slot", "side")]

        # Get the Degree value
        if not tracker.get_slot("degree"):
            degree_value = "120 degrees"
        else:
            degree_value = tracker.get_slot("degree")

        # Get the Time value
        if not tracker.get_slot("time"):
            time_value = "5 seconds"
        else:
            time_value = tracker.get_slot("time")

        # Get the side value
        side_value = tracker.get_slot("side")

        # Handle degree entity
        degree_info = process_degree_value(degree_value, dispatcher)

        # if the value returned from process_degree_value() is none, re ask for the degree entity
        if degree_info is None:
            return [SlotSet("requested_slot", "degree")]

        # Handle time entity
        time_info = resolve_time(time_value)

        #create a json array to store the data
        json_response = {"text":f"I'm raising my {side_value} hand",
                        "entities":{"side":side_value,"degree_value":degree_info,"time_value":time_info},
                        "intent": intent,
                        "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

        #reset the slots for the new request
        return [SlotSet("degree", None), SlotSet("time", None), SlotSet("side", None), SlotSet("requested_slot", None)]

def process_degree_value(degree_value: str, dispatcher:CollectingDispatcher) -> str:
    # load the model
    with open('svm_model.pkl', 'rb') as file:
        loaded_svm_model = pickle.load(file)
        test_sentences = get_sentence_embedding([degree_value])
        y_pred = loaded_svm_model.predict(test_sentences)
        print(f"predict {y_pred[0]}")

    #check if the pridicted degree is true
    if y_pred[0] == 1:
        # Remove the 'degrees' keyword from the value
        degree_value = degree_value.replace("degrees", "").strip()
        return int(degree_value)
    else:
        # re-ask for degree entity
        dispatcher.utter_message(template="utter_ask_degree_again")
        return None

def resolve_time(time_value: str) -> str:
    # Check if the value contains the word 'second' or 'seconds'
    if "second" in time_value:
        return "00:00:" + re.findall(r"\d+", time_value)[0].zfill(2)

    # Check if the value contains the word 'minute' or 'minutes'
    if "minute" in time_value:
        minutes = re.findall(r"\d+", time_value)[0]
        return "00:" + minutes.zfill(2) + ":00"

    # Check if the value contains the word 'hour' or 'hours'
    if "hour" in time_value:
        hours = re.findall(r"\d+", time_value)[0]
        return hours.zfill(2) + ":00:00"

    return "Invalid time format"


# actions for chatbot mouvments

class ActionGreetingMouvment(Action):
    def name(self) -> Text:
        return "action_greeting_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "Hello"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionGoodbyeMouvment(Action):
    def name(self) -> Text:
        return "action_goodbye_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "Bye"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionThanksMouvment(Action):
    def name(self) -> Text:
        return "action_thanks_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "You are welcome"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionLaughMouvment(Action):
    def name(self) -> Text:
        return "action_laugh_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "hahaha"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionDanceMouvment(Action):
    def name(self) -> Text:
        return "action_dance_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "okayy!"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionLikeMouvment(Action):
    def name(self) -> Text:
        return "action_like_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "Sure"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionPhotoMouvment(Action):
    def name(self) -> Text:
        return "action_photo_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "Say Cheese!"
        degree = ""
        time = ""
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

class ActionJokeMouvment(Action):
    def name(self) -> Text:
        return "action_joke_mouvment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "Why couldn't the leopard play hide and seek? Because he was always spotted!",
            "How does a penguin build its house? Igloos it together!",
            "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fish with no eyes? Fsh!"
        ]
        text = random.choice(jokes)
        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)


class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Reset the slots and requested slot
        events = [
            SlotSet(slot, None) for slot in ["degree", "time", "side", "requested_slot"]
        ] + [SlotSet("requested_slot", None)]

        # Check if the latest user message was the cancel intent
        if tracker.latest_message.get("intent", {}).get("name") == "cancel_conversation":
            events += [
                UserUtteranceReverted(),  # Revert the latest user message
                SlotSet("degree", None),  # Reset the degree slot
                SlotSet("time", None),  # Reset the time slot
                SlotSet("side", None),  # Reset the side slot
                SlotSet("username", None), # Reset the username slot
                SlotSet("requested_slot", None),  # Reset the requested_slot slot
                Restarted(),  # Trigger a restart of the conversation
                dispatcher.utter_message(template="utter_cancelled")  # Send cancellation message
            ]
        else:
            events.append(ActionExecuted("action_listen"))  # Listen for user input

        return events
    
class ActionMimicHand(Action):
    def name(self) -> Text:
        return "action_mimic_hand"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )->List[Dict[Text, Any]]:
        # get the intent name
        intent = tracker.latest_message.get("intent", {}).get("name")

        #create a json array to store the data
        json_response = {"text":"I'm mimicking your hand mouvement",
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

        return []

# class ValidateUsernameForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_username_form"

#     def extract_username(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
#         # Code here
#         # return {"username":"test"}
#         dispatcher.utter_message(text=f"in extract slot:{tracker.latest_message.get('text')}")
#         return {"username":tracker.latest_message.get("text")}
#         # dispatcher.utter_message(text=f"username slot:{tracker.get_slot('username')}")
#         # if tracker.latest_message.get('text') == "samir":
#         #     dispatcher.utter_message(text="in if")
#         #     return {"username": tracker.latest_message.get("text")}
#         # else:
#         #     dispatcher.utter_message(text="in else")
#         #     return [SlotSet("requested_slot","username")]    

#     def validate_username(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
#     # Code here
#         dispatcher.utter_message(text="in validate username slot")
#         dispatcher.utter_message(f"username={tracker.get_slot('username')}")
#         if tracker.get_slot("username") == "ask_for_user_name":
#             return {"username": None}
#         else:
#             return {"username": tracker.latest_message.get("text")}
#         # return {"username": None}
    

class ActionUsernameValue(Action):
    def name(self) -> Text:
        return "action_username_value"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # return [SlotSet("username", None), SlotSet("username_confirmation", None)]
        username_slot = tracker.get_slot("username")
        username_confirm = tracker.get_slot("username_confirmation")

        dispatcher.utter_message(f"in username action, username={username_slot}, confirmation = {username_confirm}")
        #check if the entry is a name using model (check_username_model(text))
        #if true save it in the slot
        # if text == "samir": #replace this by if the returned value of the model is true
        #     SlotSet("username",text)
        # else:
        #     dispatcher.utter_message(template="utter_ask_username")
        #     return [SlotSet("requested_slot", "username")]
        #check if the entry is a name using model (check_username_confirm_model(text))
        #if true save it in the slot
        # if text == "yes": #replace this by if the returned value of the model is true
        #     SlotSet("username_confirmation", text)
        # else:
        #     dispatcher.utter_message(template="utter_ask_username_confirmation")
        #     return [SlotSet("requested_slot", "username_confirmation")]
        
        return [SlotSet("username", None),SlotSet("username_confirmation", None)]

def username_confirmation(dispatcher, tracker):
    confirm = tracker.get_slot("username_confirmation")
    if confirm:
        print("---------- in username confirmation ----------")
        if confirm.lower() == "yes":
            return "yes"
        else:
            return "no"
    
    print("in not confirm")
    # dispatcher.utter_message(template="utter_ask_username_confirmation")
    return [FollowupAction("action_get_user_confirmation")]
    
class ActionGetUserConfirmation(Action):
    def name(self) -> Text:
        return "action_get_user_confirmation"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("******** in username confirm ************")
         # Get the user input
        user_input = tracker.latest_message.get("text")

        # Check if the user confirms or not
        if user_input.lower() == "yes":
            return [SlotSet("username_confirmation", "yes"), FollowupAction("action_ask_username")]
        elif user_input.lower() == "no":
            dispatcher.utter_message(text="Okay, let me know if you change your mind.")
            return [SlotSet("username", None), SlotSet("requested_slot", None), SlotSet("username_confirmation", "no")]
        else:
            dispatcher.utter_message(template="utter_ask_username_confirmation")
            return [SlotSet("requested_slot", "username_confirmation")]
        # dispatcher.utter_message(template="utter_ask_username_confirmation")
        # return [SlotSet("requested_slot", "username_confirmation"), UserUtteranceReverted()]

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the user's name from the slot
        user_name = tracker.get_slot("username")
        print(f"greet username {user_name}")

        if user_name:
            # Greet the user using their name
            dispatcher.utter_message(template="utter_greet_user", name=user_name)
        else:
            # If the user's name is not available, use a default greeting
            dispatcher.utter_message(text="Hello! How can I assist you today?")

        return []
    
import socket
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
            category = tracker.get_slot("category")
            # Create a dictionary to store the category
            data = {
                "category": category
            }
            
            # Serialize the dictionary as JSON
            data_json = json.dumps(data)

            # Send the message to the server
            client_socket.send(message.encode("utf-8"))
            client_socket.send(data_json.encode("utf-8"))


            # Receive and print the response from the server
            response = client_socket.recv(1024).decode("utf-8")
            intent_name = "conversation"
            json_response = {
                "intent": intent_name,
                "gpt_response": response
            }
            json_response = json.dumps(json_response)
            dispatcher.utter_message(text=json_response)
        except Exception as e:
            print("Error:", str(e))
        finally:
            client_socket.close()  # Close the socket
        return []
        # try:
        #     # Create a socket
        #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     client_socket.connect(("localhost", 8887))  # Connect to the server's IP and port
            
        #     message = tracker.latest_message.get('text')
        #     print("in soket")
        #     # Send the message to the server
        #     client_socket.send(message.encode("utf-8"))
            
        #     # Receive and print the response from the server
        #     response = client_socket.recv(1024).decode("utf-8")
        #     intent_name = "conversation"
        #     json_response = {
        #         "intent": intent_name,
        #         "gpt_response": response
        #     }
        #     json_response = json.dumps(json_response)
        #     dispatcher.utter_message(text=json_response)
        # except Exception as e:
        #     print("Error:", str(e))
        # finally:
        #     client_socket.close()  # Close the socket
        # return []

class ActionRockPaperGame(Action):
    def name(self) -> Text:
        return "action_rockpaper_game"


    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Let's start")

        jsonRocker = {
            "degree": "90",
            "action": "Rocker",
            "time" :  "3",
        }

        jsonPeaper = {
            "degree": "90",
            "action": "Peaper",
            "time" :  "3",
        }

        jsonSeaser = {
            "degree": "90",
            "action": "Seaser",
            "time" :  "3",
        }

        jsonPeaper = json.dumps(jsonPeaper)
        jsonSeaser = json.dumps(jsonSeaser)
        jsonRocker = json.dumps(jsonRocker)


        choice = [jsonPeaper,jsonRocker,jsonSeaser]
        game = random.choice(choice)
        dispatcher.utter_message(text=game)
        return []

class ActionProvideInfo(Action):
    def name(self) -> Text:
        return "action_provide_information"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )-> List[Dict[Text, Any]]:
        print(f"category slot: {tracker.get_slot('category')}")
        dispatcher.utter_message(template="utter_provide_information")
        return []