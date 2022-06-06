import requests
import redis
import logging
import json
import os
import re
from django.conf import settings
from typing import List, Dict, Union, Any

BASE_DIR = settings.BASE_DIR
REDIS_TIMEOUT = settings.REDIS_TIMEOUT
REDIS_PORT = settings.REDIS_PORT
REDIS_HOST = settings.REDIS_HOST
API_KEY = settings.API_KEY

logging.basicConfig(filename="util_errors.txt",
                    filemode='a',
                    format="%(asctime)s %(levelname)s-%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def get_cache_connection() -> Union[object, None]:
    try:
        cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        return cache
    except Exception as e:
        logging.error(e)
        return None


def get_language(get_request: Dict[str, Any]) -> str:
    if get_request.get("lang", "") in ["en", "fr", "de"]:
        return get_request.get("lang", "")
    else:
        return "en"


def get_context(lang: str) -> str:
    with open(os.path.join(BASE_DIR, "languages", f"{lang}.json"), encoding='utf-8') as file:
        return json.loads(file.read())


def get_valid_input(post_request: Dict[str, Any]):
    input = re.split("\t|,|\s+|;", post_request.get("city").strip())[:2]
    valid_input = {}
    if len(input) == 2:
        valid_input["city"], valid_input["country"] = input[0], input[1]
    else:
        valid_input["city"], valid_input["country"] = input[0], ""
    return valid_input


def get_value_from_cache(cache: object, input: Dict[str, str], lang: str) -> Union[Dict[str, Any], None]:
    value = cache.get(f"{input['city']}_{input['country']}_{lang}")
    if value:
        cur_weather_dict = json.loads(value.decode("utf-8"))
        print("found in cache", cache.ttl(f"{input['city']}_{input['country']}_{lang}"))
        return cur_weather_dict
    else:
        return None


def get_value_from_API(context: Dict[str, str], input: Dict[str, str], lang: str) -> Union[str, None]:
    print("input: ",input)
    if input['city'] == "":
        context["error_msg"] = context["error_msg_3"]
        logging.error(context["error_msg"])
        return None
    api_response = requests.get(
        (f"https://api.openweathermap.org/data/2.5/weather?"
         f"q={input['city']},{input['country']}&"
         f"lang={lang}&"
         f"units=metric&"
         f"appid={API_KEY}"))
    print("api_respomse: ",api_response)
    context["api_error_msg"] = json.loads(api_response.text).get("message")
    print("context: ",context)
    if api_response.status_code == 404:
        context["error_msg"] = context["error_msg_1"]
        logging.error(context["error_msg"])
        return None
    elif api_response.status_code != 200:
        context["error_msg"] = context["error_msg_2"]
        logging.error(context["error_msg"])
        return None
    elif api_response.status_code == 200:
        return json.loads(api_response.text)


def set_value_in_cache(cache: object, input: Dict[str, str], lang: str, cur_weather_dict: Dict[str, Any]) -> None:
    cache.psetex(f"{input['city']}_{input['country']}_{lang}",
                 REDIS_TIMEOUT,
                 json.dumps(cur_weather_dict))


def update_context_with_data(context: Dict[str, str], cur_weather_dict: Dict[str, Any], lang: str) -> None:
    context["lang"] = "fr-FR" if lang == "fr" else "de-DE" if lang == "de" else "en-US"
    context["name"] = cur_weather_dict.get("name")
    context["country"] = cur_weather_dict["sys"]["country"]
    context["temp"] = cur_weather_dict.get("main", "").get("temp")
    context["min_temp"] = cur_weather_dict.get("main", "").get("temp_min", "")
    context["max_temp"] = cur_weather_dict.get("main", "").get("temp_max", "")
    context["humidity"] = cur_weather_dict.get("main", "").get("humidity", "")
    context["pressure"] = cur_weather_dict.get("main", "").get("pressure", "")
    context["wind_speed"] = cur_weather_dict.get("wind", "").get("speed", "")
    context["wind_direction"] = wind_direction(cur_weather_dict.get("wind", "").get("deg", ""))
    context["description"] = cur_weather_dict.get("weather", "")[0].get("description", "")
    print("context_updated: ",context)


def wind_direction(deg: int) -> str:
    if deg >= 348.75 or deg < 11.25:
        direction = "N"
    elif deg >= 11.25 or deg < 33.75:
        direction = "NNE"
    elif deg >= 33.75 or deg < 56.25:
        direction = "NE"
    elif deg >= 56.25 or deg < 78.75:
        direction = "ENE"
    elif deg >= 78.75 or deg < 101.25:
        direction = "E"
    elif deg >= 101.25 or deg < 123.75:
        direction = "ESE"
    elif deg >= 123.75 or deg < 146.25:
        direction = "SE"
    elif deg >= 146.25 or deg < 168.75:
        direction = "SSE"
    elif deg >= 168.75 or deg < 191.25:
        direction = "S"
    elif deg >= 191.25 or deg < 213.75:
        direction = "SSW"
    elif deg >= 213.75 or deg < 236.25:
        direction = "SW"
    elif deg >= 236.25 or deg < 258.75:
        direction = "WSW"
    elif deg >= 258.75 or deg < 281.25:
        direction = "W"
    elif deg >= 281.25 or deg < 303.75:
        direction = "WNW"
    elif deg >= 303.75 or deg < 326.25:
        direction = "NW"
    elif deg >= 326.25 or deg < 348.75:
        direction = "NNW"
    else:
        direction = "Not Available"
    return direction
