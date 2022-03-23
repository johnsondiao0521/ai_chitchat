
from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet
from actions.weatherapis import get_weather_by_day
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout


class NumberForm(FormValidationAction):

    def name(self) -> Text:
        return "number_form"

    def required_slots(self, tracker) -> List[Text]:
        return ["type", "number", "business"]

    def extract_other_slots(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if not slot_to_fill:
            return super().extract_other_slots(dispatcher, tracker, domain)
        else:
            return {}

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type": self.from_entity(entity="type", not_intent="chitchat"),
            "number": self.from_entity(entity="number", not_intent="chitchat"),
            "business": [
                self.from_entity(entity="business", intent=["inform", "request_number"]),
                self.from_entity(entity="business")
            ]
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        number_type = tracker.get_slot("type")
        number = tracker.get_slot("number")
        business = tracker.get_slot("business")
        if not business:
            dispatcher.utter_message(text="您要查询的{}{}所属人为张三，湖南长沙人，现在就职于地球村物业管理有限公司。".format(number_type, number))
            return []
        dispatcher.utter_message(text="你要查询{}为{}的{}为：balabalabalabalabala。".format(number_type, number, business))
        return [SlotSet("business", None)]


class WeatherForm(FormValidationAction):
    def name(self) -> Text:
        return "weather_form"

    def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        return ["date_time", "address"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict]:
        address = tracker.get_slot("address")
        data_time = tracker.get_slot("data_time")

        data_time_number = text_date_to_number_date(data_time)
        if isinstance(data_time_number, str):
            dispatcher.utter_message("暂不支持查询 {} 的天气".format([address, data_time_number]))
        else:
            weather_data = get_text_weather_date(address, data_time, data_time_number)
            dispatcher.utter_message(weather_data)
        return []


def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )

    return text_message


def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # TODO: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # TODO: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="您好搞笑啊，怎么跑到我这个山沟里来了呢 !")

        return []
