from django.shortcuts import render
from .util import *
from typing import Any


# Create your views here.
def current_data(request: object) -> object:
    lang = get_language(request.GET)
    context = get_context(lang)
    context["PORT"] = request.META['SERVER_PORT']
    print(context)
    if request.method == "POST":
        input = get_valid_input(request.POST)
        cache_conn = get_cache_connection()
        if cache_conn:
            cur_weather_dict = get_value_from_cache(cache_conn, input, lang)
        if not cur_weather_dict:
            cur_weather_dict = get_value_from_API(context, input,lang)
        if not cur_weather_dict:
            return render(request, 'index.html', context)
        set_value_in_cache(cache_conn,input,lang,cur_weather_dict)
        update_context_with_data(context, cur_weather_dict , lang)
        return render(request, 'index.html', context)
    elif request.method == "GET":
        return render(request, 'index.html', context)
