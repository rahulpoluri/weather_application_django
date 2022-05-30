

def wind_direction(deg):
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
