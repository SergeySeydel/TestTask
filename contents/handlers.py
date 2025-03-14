import datetime
import json
from typing import Union

from ru.travelfood.simple_ui import NoSQL as noClass


class hashMap:
    def get(self, key: str) -> str:
        

        pass

    def put(self, key: str, value: str):
        

        pass

    def containsKey(self, key: str) -> bool:
        

        pass

    def remove(self, key: str):
        

        pass


class DB:
    def get(self, key: str) -> str:
        

        pass

    def put(self, key: str, value: Union[str, bool, int], register: bool):
        

        pass

    def delete(self, key: str):
       

        pass

    def getallkeys(self) -> str:
        

        pass


db_all_birds: DB = noClass("birds")
db_birds_which_i_saw: DB = noClass("birds_which_i_saw")

def birds_screen(hashMap: hashMap, _files=None, _data=None):
    

    birds_cards = {"customcards": {
        "options": {
          "search_enabled": True,
          "save_position": True
        },

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@bird_picture",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "match_parent",
                            "height": "wrap_content",
                            "weight": 1
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_name",
                                    "NoRefresh": False,
                                    "TextSize": "16",
                                    "TextColor": "#ca6702",
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "gravity_horizontal": "left",
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_color",
                                    "NoRefresh": False,
                                    "TextSize": "16",
                                    "TextColor": "#ca6702",
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "gravity_horizontal": "left",
                                },
                            ]
                        },
                    ]
                },
            ]
        }
        }
    }

    birds_cards["customcards"]["cardsdata"] = []

    keys_str = db_all_birds.getallkeys()
    keys = json.loads(str(keys_str).encode("utf-8"))
    for key in keys:
        bird = get_bird_data_by_key(key=key)
        bird["bird_name"] = "Название птицы: " + key
        bird["bird_color"] = "Цвет перьев птицы: " + bird.get("bird_color")
        birds_cards["customcards"]["cardsdata"].append(bird)
    hashMap.put(
        "cards",
        json.dumps(birds_cards, ensure_ascii=False)
    )
    return hashMap

def add_bird_screen(hashMap: hashMap, _files=None, _data=None):
    

    hashMap.put("ShowScreen", "Добавление птицы")
    return hashMap


def create_bird(hashMap: hashMap, _files=None, _data=None):
    

    bird_name = hashMap.get("bird_name")

    
    if db_all_birds.get(bird_name):
        hashMap.put("toast", "Птица уже в базе")
        return hashMap

    bird_color = hashMap.get("bird_color")

    if bird_name == "" or bird_color == "":
        hashMap.put("toast", "Поле название и цвет обязательные")
        return hashMap

    bird_data = {
        "bird_color": bird_color,
        "bird_picture": hashMap.get("photo"),
    }
    db_all_birds.put(
        bird_name,
        json.dumps(bird_data, ensure_ascii=False),
        True
    )

    hashMap.put("toast", f"Птица {bird_name} создана")

    remove_bird_info_from_hashMap(hashMap=hashMap)

    return hashMap


def show_one_bird(hashMap: hashMap, _files=None, _data=None):
    

    hashMap.put("ShowScreen", "Птица")
    bird_name = hashMap.get("selected_card_key")

    bird_data = get_bird_data_by_key(key=bird_name)

    hashMap.put("bird_name", bird_data.get("bird_name"))
    hashMap.put("bird_color", bird_data.get("bird_color"))
    hashMap.put("bird_picture", bird_data.get("bird_picture"))

    return hashMap


def delete_bird(hashMap: hashMap, _files=None, _data=None):
    

    bird_name = hashMap.get("selected_card_key")
    db_all_birds.delete(bird_name)
    hashMap.put("toast", f"Птица {bird_name} удалена из БД.")
    hashMap.put("ShowScreen", "Список птиц")

    remove_bird_info_from_hashMap(hashMap=hashMap)

    return hashMap


def add_seen_bird(hashMap: hashMap, _files=None, _data=None):
    

    if (
        hashMap.containsKey("_birds_which_i_saw") and
        hashMap.get("_birds_which_i_saw") is not None
    ):
        birds_which_i_saw = hashMap.get("_birds_which_i_saw")
        birds_which_i_saw += "," + hashMap.get("selected_card_key")
        hashMap.put("_birds_which_i_saw", birds_which_i_saw)
    else:
        hashMap.put("_birds_which_i_saw", hashMap.get("selected_card_key"))

    hashMap.put(
        "toast",
        f"Птица: {hashMap.get('selected_card_key')} добавлена в список"
    )
    return hashMap




def get_bird_data_by_key(key: str) -> dict:
    

    bird_data_str = db_all_birds.get(key)
    bird_data = json.loads(bird_data_str)
    bird = {
        "key": key,
        "bird_name": key,
        "bird_color": bird_data.get("bird_color"),
        "bird_picture": bird_data.get("bird_picture"),
    }
    return bird


def remove_bird_info_from_hashMap(hashMap: hashMap):
    

    hashMap.remove("bird_name")
    hashMap.remove("bird_color")
    hashMap.remove("photo")

    return hashMap

def show_birds_seen_screen(hashMap: hashMap, _files=None, _data=None):
    

    birds_cards = {"customcards": {
        "options": {
          "search_enabled": True,
          "save_position": True
        },

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@bird_picture",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "BackgroundColor": "",
                            "width": "match_parent",
                            "height": "wrap_content",
                            "weight": 1
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@bird_name",
                                    "NoRefresh": False,
                                    "TextSize": "16",
                                    "TextColor": "#ca6702",
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "weight": "",
                                    "gravity_horizontal": "left",
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@count_saw",
                                    "NoRefresh": False,
                                    "TextSize": "16",
                                    "TextColor": "#ca6702",
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "gravity_horizontal": "left",

                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "TextColor": "#ca6702",
                                    "Value": "@updated_date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "gravity_horizontal": "left",
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "TextColor": "#ca6702",
                                    "Value": "@created_date",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "Variable": "",
                                    "gravity_horizontal": "left",
                                },
                            ]
                        },
                    ]
                },
            ]
         }
        }
    }

    birds_cards["customcards"]["cardsdata"] = []

    keys_str = db_birds_which_i_saw.getallkeys()
    keys = json.loads(str(keys_str).encode("utf-8"))
    for key in keys:
        bird_data_str = db_birds_which_i_saw.get(key)
        bird_data = json.loads(bird_data_str)
        obj = {
            "key": key,
            "bird_name": "Название птицы: " + key,
            "bird_picture": bird_data.get("bird_picture"),
            "count_saw": "Видел раз: " + str(bird_data.get("count_saw")),
            "updated_date": (
                "Дата обновления: " + bird_data.get("updated_date")
            ),
            "created_date": "Дата создания: " + bird_data.get("created_date"),
        }
        birds_cards["customcards"]["cardsdata"].append(obj)
    hashMap.put(
        "cards",
        json.dumps(birds_cards, ensure_ascii=False)
    )
    return hashMap


def create_seen_birds(hashMap: hashMap, _files=None, _data=None):


    if (
        hashMap.containsKey("_birds_which_i_saw") and
        hashMap.get("_birds_which_i_saw") is not None
    ):
        birds_which_i_saw = hashMap.get("_birds_which_i_saw").split(",")
    else:
        hashMap.put("toast", "Список птиц на добавление пуст")
        return hashMap

    for bird in birds_which_i_saw:
        new_bird_data = get_bird_data_for_saw(bird)
        db_birds_which_i_saw.put(
            bird,
            json.dumps(new_bird_data, ensure_ascii=False),
            True
        )

    _birds_which_i_saw = hashMap.get("_birds_which_i_saw")
    hashMap.put("toast", f"Добавлены птицы: {_birds_which_i_saw}")

    hashMap.put("_birds_which_i_saw", None)

    return hashMap

def get_bird_data_for_saw(bird: str) -> dict:

    bird_data_str = db_birds_which_i_saw.get(bird)
    if bird_data_str:
        bird_data = json.loads(bird_data_str)
    else:
        bird_data_from_dab = db_all_birds.get(bird)
        bird_data = json.loads(bird_data_from_dab)

    updated_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    created_date = (
        bird_data.get("created_date") if bird_data_str
        else datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    )
    bird_pciture = bird_data.get("bird_picture")
    count_saw = int(bird_data.get("count_saw")) + 1 if bird_data_str else 1

    new_bird_data = {
        "updated_date": updated_date,
        "created_date": created_date,
        "bird_name": bird,
        "bird_picture": bird_pciture,
        "count_saw": count_saw
    }

    return new_bird_data