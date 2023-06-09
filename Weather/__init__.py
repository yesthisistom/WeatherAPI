from .run_query import RequestType, make_request, RequestFailed


def get_coordinate_from_city(city, state):
    params = {'q': f"{city}, {state}", }
    url = "https://geocode.maps.co/search?"
    try:
        results = make_request(url, params=params)
    except RequestFailed:
        return None

    # Make sure we get expected results
    if type(results) != list or len(results) == 0:
        return None

    # Filtered
    admin = [x for x in results if x['type'] == "administrative"]
    if len(admin) == 0:
        return None

    # Get the top administrative result
    if 'lat' not in admin[0] or 'lon' not in admin[0]:
        return None

    return admin[0]['lat'], admin[0]['lon']


def get_hourly_weather(lat, lon):
    # First get the grid values
    url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        results = make_request(url)
    except RequestFailed:
        return None

    if 'properties' not in results:
        return None

    for val in ['gridX', 'gridY', 'cwa']:
        if val not in results['properties']:
            return None

    # Get the actual weather
    gridx = results['properties']['gridX']
    gridy = results['properties']['gridY']
    office = results['properties']['cwa']
    url = f"https://api.weather.gov/gridpoints/{office}/{gridx},{gridy}/forecast/hourly"

    try:
        results = make_request(url)
    except RequestFailed:
        return None

    return [x for x in results['properties']['periods']]


def get_aqi(lat, lon):
    token = os.getenv('API_USER')
    if not token:
        return None

    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    payload = {"token": token}
    try:
        r = make_request(url, params=payload)
        return r['data']['aqi']
    except RequestFailed:
        return None


def gross_out(high, low, precipitation, aqi):
    # Gross Air
    if aqi > 150:
        return True, "Air is bad"

    # Too Cold
    if low < 10:
        return True, "It's too cold, get under a blanket"

    # Cold and Rainy
    if low > 32 and high < 50 and sum(precipitation) > len(weather_hourly) * 80:
        return True, "It's cold and rainy, get under a blanket"

    return False


def get_suggestion(weather, aqi):
    # Filter down to the next 8 hours
    weather = weather[0:8]

    temps = [x['temperature'] for x in weather]
    low, high = min(temps), max(temps)
    precipitation = [x['probabilityOfPrecipitation']['value'] for x in weather]

    if gross_out(high, low, precipitation, aqi):
        return "Sweatpants - " + gross_out(high, low, precipitation, aqi)[1]

    if high > 70:
        resp = "Summer clothes"
        if low < 70:
            resp += ", but bring sleeves"
    elif high > 60:
        resp = "Something light but with sleeves"
        if low < 50:
            resp += ", and bring a fleece"
    elif high > 45:
        resp = "Fall clothes (pants and a fleece)"
        if low < 45:
            resp += ", but bring a hat and gloves"
    elif high > 25:
        resp = "Winter things"
    else:
        resp = "Bundle up, its cold"

    if max(precipitation) > 80:
        resp += ". A raincoat is a good idea."
    elif max(precipitation) > 50:
        resp += ", and bring an umbrella."

    return resp



