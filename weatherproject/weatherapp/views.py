from django.shortcuts import render
from django.conf import settings
import requests
import json, re, os
from .util import wind_direction
from django.core.cache import cache

BASE_DIR = settings.BASE_DIR
REDIS_TIMEOUT = settings.REDIS_TIMEOUT

# Create your views here.
def current_data(request):
    print(request.GET.get("lang"))
    print(request.POST)
    lang = request.GET.get("lang", "") if request.GET.get("lang", "") in ["en", "fr", "de"] else "en"
    with open(os.path.join(BASE_DIR, "languages", f"{lang}.json"), encoding='utf-8') as file:
        context = json.loads(file.read(), )
    context["lang"] = "fr-FR" if lang == "fr" else "de-DE" if lang == "de" else "en-US"
    if request.method == "POST":
        input = re.split("\t|,|\s+|;", request.POST.get("city").strip())[:2]
        if len(input) == 2:
            city, country = input[0], input[1]
        else:
            city, country = input[0], ""
        
        if cache.get(f"{city}_{country}_{lang}"):
            cur_weather_dict = cache.get(f"{city}_{country}_{lang}")
            print("found in cache", cache.ttl(f"{city}_{country}_{lang}"))
        else:
            api_response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&lang={lang}&units=metric&appid=014ec5fe82d5d8d60b5df7a9a9fbd325")
            if api_response.status_code is not 200:
                context["error_msg"] = json.loads(api_response.text).get("message")
                return render(request, 'index.html', context)
            print(api_response)
            cur_weather_dict = json.loads(api_response.text)
            cache.set(f"{city}_{country}_{lang}",cur_weather_dict,timeout=REDIS_TIMEOUT)

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
        print(context)
        return render(request, 'index.html', context)
    elif request.method == "GET":
        return render(request, 'index.html', context)
