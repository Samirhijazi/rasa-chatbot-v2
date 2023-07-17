from typing import Any, Text, Dict, List, Union
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionExecuted, Restarted
from rasa_sdk.executor import CollectingDispatcher
import re
import pickle
from actions.degree_model.bert_model import get_sentence_embedding

import json

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
        # check if the degrees entity contains one world (for example only the number 23)
        degree_entity_one_word = bool(re.match(r'^\w+$', tracker.get_slot("degree")))

        # Check if the required slots are filled or the degrees entity contains only the number
        if not tracker.get_slot("degree") or degree_entity_one_word or not tracker.get_slot("time") or not tracker.get_slot("side"):
            # If any of the required slots are missing, ask the user to provide the missing values
            if not tracker.get_slot("degree") or degree_entity_one_word:
                dispatcher.utter_message(template="utter_ask_degree")
                return [SlotSet("requested_slot", "degree")]
            elif not tracker.get_slot("time"):
                dispatcher.utter_message(template="utter_ask_time")
                return [SlotSet("requested_slot", "time")]
            else:
                dispatcher.utter_message(template="utter_ask_side")
                return [SlotSet("requested_slot", "side")]

        # Get the slot values
        degree_value = tracker.get_slot("degree")
        time_value = tracker.get_slot("time")
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
                         "intent": intent}
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
        return degree_value
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
                         "intent": intent}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

        return []