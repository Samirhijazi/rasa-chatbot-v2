from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionExecuted, Restarted, AllSlotsReset, FollowupAction
import re
import pickle
import random  
from actions.degree_model.bert_model import get_sentence_embedding
import json
import spacy
from langdetect import detect
from actions.username_model.translate import translateToEnglish
import langid

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

        #check intent to send the response according to the language
        if intent == "raise_hand":
            text = f"I'm raising my {side_value} hand"
        else:
            text = f"رح علي ايدي {side_value}"
        print(f"text {text}")
        #create a json array to store the data
        json_response = {"text": text,
                        # "text":f"I'm raising my {side_value} hand",
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
        # degree_value = degree_value.replace("degrees", "").strip()
        words = degree_value.split()
        number_value = words[0]
        return int(number_value)
    else:
        # re-ask for degree entity
        dispatcher.utter_message(template="utter_ask_degree_again")
        return None

def resolve_time(time_value: str) -> str:
    # Check if the value contains the word 'second' or 'seconds'
    # if "second" in time_value:
    return "00:00:" + re.findall(r"\d+", time_value)[0].zfill(2)

    # Check if the value contains the word 'minute' or 'minutes'
    # if "minute" in time_value:
    #     minutes = re.findall(r"\d+", time_value)[0]
    #     return "00:" + minutes.zfill(2) + ":00"

    # Check if the value contains the word 'hour' or 'hours'
    # if "hour" in time_value:
    #     hours = re.findall(r"\d+", time_value)[0]
    #     return hours.zfill(2) + ":00:00"

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
        if intent == "greeting":
            text = "Hello"
        else:
            text = "مرحبا"
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
        if intent == "goodbye":
            text = "Bye"
        else:
            text = "ال اللقاء"
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
        if intent == "thanks":
            text = "You are welcome"
        else:
            text = "تكرم"
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
        if intent == "laugh":
            text = "hahaha"
        else:
            text = "هاهاها"
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
        if intent == "dance":
            text = "okayy!"
        else:
            text = "حسنا"
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
        if intent == "like":
            text = "Sure"
        else:
            text = "أكيد"
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
        if intent == "take a photo":
            text = "Say Cheese!"
        else:
            text = "ضحاك"
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
        if intent == "joke":
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
        else:
            jokes = [
                "لماذا لا يثق العلماء في الذرات؟ لأنها تشكل كل شيء!",
                "الخطوط المتوازية لديها الكثير من التشابه. من المؤسف أنها لن تلتقي أبدًا.",
                "لماذا فاز دمية الحشائش بجائزة؟ لأنه كان متميزًا في ميدانه!",
                "أنا أقرأ كتابًا عن مكافحة الجاذبية. من المستحيل أن تضعه!",
                "لماذا سقطت الدراجة؟ لأنها كانت متعبة جدًا!",
                "لماذا لم يستطع الفهد لعب الاختباء وراء الظهر؟ لأنه كان دائمًا مرئيًا!",
                "كيف يبني البطريق منزله؟ إنه يجمع بينهما!",
                "قلت لزوجتي إنها ترسم حواجبها مرتفعة جدًا. بدت متفاجئة.",
                "لماذا لا يقاتل الهياكل العظمية بعضها البعض؟ ليس لديهم الجرأة!",
                "ماذا تسمي سمكة بدون عيون؟ سمكة!"
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
        ]

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
        elif tracker.latest_message.get("intent", {}).get("name") == "cancel_conversation_ar":
            events += [
                UserUtteranceReverted(),  # Revert the latest user message
                SlotSet("degree", None),  # Reset the degree slot
                SlotSet("time", None),  # Reset the time slot
                SlotSet("side", None),  # Reset the side slot
                SlotSet("username", None), # Reset the username slot
                SlotSet("requested_slot", None),  # Reset the requested_slot slot
                Restarted(),  # Trigger a restart of the conversation
                dispatcher.utter_message(template="utter_cancelled_ar")  # Send cancellation message
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
        if intent == "mimic_my_hand":
            text = "I'm mimicking your hand mouvement"
        else:
            text = "اوكي, عم قلدك"

        #create a json array to store the data
        json_response = {"text":text,
                         "intent": intent,
                         "inputHint": "acceptingInput"}
        json_response = json.dumps(json_response)

        #send the json array
        dispatcher.utter_message(text=json_response)

        return []
    
class ActionUsernameValue(Action):
    def name(self) -> Text:
        return "action_username_value"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # get  the values of username and confirmation slots
        # if tracker.get_slot("username_value"):
        #     username_slot = tracker.get_slot("username_value")
        # else:
        username_slot = tracker.get_slot("username")
        print(f"username value {username_slot}")
        username_confirm = tracker.get_slot("username_confirmation")
        
        detected_lang, _ = langid.classify(username_slot) # detect if the input is in english or in arabic
        if len(username_slot.split()) <= 2:
            if detected_lang == "ar":
                text = f"مرحبا {username_slot}"
            else:
                text = f"Hello {username_slot}"
        else:
            # load the model of username
            # detected_lang, _ = langid.classify(username_slot) # detect if the input is in english or in arabic
            # print(f"detected lang of username is {detected_lang}")
            if detected_lang == "ar":
                username_slot = add_name_to_sentence(tracker.get_slot("username"))
            print(f"username after add name sentence is {username_slot}")
            if detected_lang == "ar":
                username_slot = nlp1(translateToEnglish(username_slot))
            else:
                username_slot = nlp1(username_slot)
            print(f"username after translate is {username_slot}")
            if username_slot.ents:
                username_slot = str(username_slot.ents[0])
                print(f"username ents is {username_slot}")
            else:
                print("No username entity found")
                return [SlotSet("username", None), SlotSet("username_confirmation", None)]
            if len(username_slot) == 0:
                return [SlotSet("requested_slot", "username")]
        
        # load the model of confirmation
        detected_lang_confirm, _ = langid.classify(username_confirm) # detect if the input of confirmation is in english or in arabic
        if detected_lang_confirm == "ar":
            username_confirm = translateToEnglish(username_confirm) # translate the confirmation message to english
        print(f"username confirm : {username_confirm}")
        confirm_pred = get_confirmation_pred(username_confirm,tracker)
        if confirm_pred is None:
            dispatcher.utter_message(text="give me 'name is not recognized' to retry the scenario")
            return [SlotSet("username", None), SlotSet("username_confirmation", None)]

        if detected_lang == "ar":
            text = f"مرحبا {username_slot}"
        else:
            text = f"Hello {username_slot}"
        json_array = {
            "text": text,
            "name": username_slot,
            "intent": "new_user"
        }
        print(f"text : {text}")
        json_array = json.dumps(json_array)
        dispatcher.utter_message(text=json_array)
        # reset the username and confirmation slots
        return [SlotSet("username",None), SlotSet("username_confirmation", None)]
        
def get_confirmation_pred(confirm_value: str,tracker:Tracker) -> str:
    # load the model
    with open('confirm_model.pkl', 'rb') as file:
        loaded_svm_model = pickle.load(file)
        test_sentences = get_sentence_embedding([confirm_value])
        y_pred = loaded_svm_model.predict(test_sentences)
        print(f"predict {y_pred[0]}")

    if y_pred[0] == 1:
        return 1
    else:
        return None
    
def add_name_to_sentence(sentence):
    sentence_list = sentence.split()

    # check if the length of the sentence is less than or equal to 2
    if(len(sentence_list)) <= 2:
        sentence_list.insert(0, "اسمي") # insert اسمي at the beginning of the list
        
    new_sentence = " ".join(sentence_list) # convert the list back to a string with space-separator elements
    return new_sentence

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
            # Create a dictionary with both message and category
            data = {
                "message": message,
                "category": category
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
        intent = tracker.latest_message.get("intent", {}).get("name")
        if intent == "rock_paper_seaser" :
            dispatcher.utter_message(text="Let's start")
        else:
            dispatcher.utter_message(text="هيا لنبدأ")
            
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
        intent = tracker.latest_message.get("intent", {}).get("name")
        if  intent == "provide_information":
            dispatcher.utter_message(template="utter_provide_information")
        else :
            dispatcher.utter_message(template="utter_provide_information_ar")
            
        return []
    
class ActiongenraleInfo(Action):
    def name(self) -> Text:
        return "action_generale_information"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )-> List[Dict[Text, Any]]:
        print("slot is empty new")
        return [SlotSet("category",None)]
 
class ActionVoice(Action):
    def name(self) -> Text:
        return "action_voice"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    )-> List[Dict[Text, Any]]:
        entites = 2
        intent = tracker.latest_message.get("intent", {}).get("name")
        text = "المطبخْ. الحمّامْ.."
        json_array = {
                    "text": text,
                    "entites" : entites,
                    "intent" : intent
        } 
        json_voice = json.dumps(json_array)
        dispatcher.utter_message(json_voice)
        return[]