import Weather

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return "Weather Rest API is up and running"


@app.get("/hourly/")
def hourly(city: str, state: str):
    coord = Weather.get_coordinate_from_city(city, state)
    if not coord:
        raise HTTPException(status_code=400, detail="Unable to resolve this location")

    weather = Weather.get_hourly_weather(*coord)
    if not weather:
        raise HTTPException(status_code=404, detail=f"Unable to get weather for this coordinate: {coord[0]}, {coord[1]}")

    return weather


@app.get("/clothing_req/")
def clothing_req(city: str, state: str):
    coord = Weather.get_coordinate_from_city(city, state)
    if not coord:
        raise HTTPException(status_code=400, detail="Unable to resolve this location")
    weather = Weather.get_hourly_weather(*coord)
    if not weather:
        raise HTTPException(status_code=404, detail=f"Unable to get weather for this coordinate: {coord[0]}, {coord[1]}")

    aqi = Weather.get_aqi(*coord)
    if not aqi:
        aqi = 50  # Since we don't return this and its for a recommendation, just hardcode a nominal value

    return Weather.get_suggestion(weather, aqi)


