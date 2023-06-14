from typing import Any, Text, Dict, List
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


def text_date_to_int(text_date):
    if text_date == "today":
        return 0
    if text_date == "tomorrow":
        return 1
    if text_date == "yesterday":
        return -1

    # in other case
    return None


weekday_mapping = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def weekday_to_text(weekday):
    return weekday_mapping[weekday]


class ActionQueryTime(Action):
    def name(self) -> Text:
        return "action_query_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_time = datetime.now().strftime("It's %H:%M %p.")
        dispatcher.utter_message(text=current_time)

        return []


class ActionQueryDate(Action):
    def name(self) -> Text:
        return "action_query_date"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text_date = tracker.get_slot("date") or "today"

        int_date = text_date_to_int(text_date)
        if int_date is not None:
            delta = timedelta(days=int_date)
            current_date = datetime.now()

            target_date = current_date + delta

            dispatcher.utter_message(text=target_date.strftime("It's %B %d, %Y."))
        else:
            dispatcher.utter_message(text="The system currently doesn't support date query for '{}'".format(text_date))

        return []


class ActionQueryWeekday(Action):
    def name(self) -> Text:
        return "action_query_weekday"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text_date = tracker.get_slot("date") or "today"

        int_date = text_date_to_int(text_date)
        if int_date is not None:
            delta = timedelta(days=int_date)
            current_date = datetime.now()

            target_date = current_date + delta

            dispatcher.utter_message(text=weekday_to_text(target_date.weekday()))
        else:
            dispatcher.utter_message(text="The system currently doesn't support day of week query for '{}'".format(text_date))

        return []
    



class ActionQueryBot(Action):
    def name(self) -> Text:
        return "action_query_bot"
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get("intent", {}).get("name")
        entities = tracker.latest_message.get("entities", [])
        entity_info = [f"Entity: {entity['entity']} [{entity['value']}]" for entity in entities]
        degree_entity = next(
            (entity for entity in entities if entity["entity"] == "degree{45}"), None
        )
        time_entity = next(
            (entity for entity in entities if entity["entity"] == "time{5}"), None
        )

        if degree_entity and degree_entity['value']:
            degree_value = degree_entity['value']
            dispatcher.utter_message(text=f"{degree_entity['entity']} : {degree_value}")
            if time_entity and time_entity['value']:
                time_value = time_entity['value']
                dispatcher.utter_message(text=f"{time_entity['entity']} : {time_value}")
                return [
                    SlotSet("degree_value", degree_value),
                    SlotSet("time_value", time_value),
                ]
            else:
                missing_entity = "time"
                dispatcher.utter_message(
                    text=f"The entity '{missing_entity}' is missing. Please provide the value for '{missing_entity}'."
                )
                return [SlotSet("requested_slot", missing_entity)]
        else:
            missing_entity = "degree"
            dispatcher.utter_message(
                text=f"The entity '{missing_entity}' is missing. Please provide the value for '{missing_entity}'."
            )
            return [SlotSet("requested_slot", missing_entity)]

        # if degree_entity is not None and degree_entity['value']:
        #     dispatcher.utter_message(text=f"intent: {intent} , [ {degree_entity['entity']} : {degree_entity['value']} ]")
        # else:
        #     missing_entity = "degree{45}"
        #     dispatcher.utter_message(text=f"The entity '{missing_entity}' is missing. Please provide the value for '{missing_entity}'.")
        #     return [SlotSet("requested_slot", missing_entity)]
        #     # dispatcher.utter_message(text="entity missing")

        # if time_entity is not None and time_entity['value']:
        #     dispatcher.utter_message(text=f"Intent:{intent} , [ {time_entity['entity']} = {time_entity['value']} ]")
        # else:
        #     missing_entity = "time{5}"
        #     dispatcher.utter_message(text=f"The entity '{missing_entity}' is missing. Please provide the value for '{missing_entity}'.")
        #     return [SlotSet("requested_slot", missing_entity)]
        # # dispatcher.utter_message(text=f"Intent: {intent}, {', '.join(entity_info)}")

        # return []
    


        # intent = tracker.latest_message.get("intent", {}).get("name")
        # entities = tracker.latest_message.get("entities", [])
        # entity_info = [f"{entity['entity']} [{entity['value']}]" for entity in entities]

        # degree_entity = next(
        #     (entity for entity in entities if entity["entity"] == "degree{45}"), None
        # )

        # if not degree_entity:
        #     # Ask the user to enter the degree
        #     dispatcher.utter_message(text="Please enter the degree:")
        #     return [SlotSet("requested_slot", "degree")]

        # # Extract the degree value from the entity
        # degree_value = degree_entity["value"]

        # if degree_value:
        #     # Print the intent and entity
        #     dispatcher.utter_message(
        #         text=f"Intent: {intent}, Entity: degree [{degree_value}], Entities: {', '.join(entity_info)}"
        #     )
        # else:
        #     # Degree value is missing, ask the user to provide it
        #     dispatcher.utter_message(text="Please enter a valid degree.")

        # return [SlotSet("requested_slot", None)]


