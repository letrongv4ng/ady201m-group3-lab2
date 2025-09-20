# src/api.py
import requests

def get_coordinates_from_city(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        r = requests.get(url, params={"name": city_name, "count": 1, "language": "en", "format": "json"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            res = data["results"][0]
            return res["latitude"], res["longitude"], res["name"]
    except Exception:
        pass
    return None, None, None

def fetch_weather_data(latitude: float, longitude: float, metrics: list[str]):
    base_url = "https://api.open-meteo.com/v1/forecast"
    daily = []
    if "Temperature" in metrics:
        daily += ["temperature_2m_max", "temperature_2m_min"]
    if "Precipitation" in metrics:
        daily += ["precipitation_sum"]
    if "Wind" in metrics:
        daily += ["wind_speed_10m_max"]

    params = {
        "latitude": latitude, "longitude": longitude,
        "daily": ",".join(daily), "timezone": "auto",
        "forecast_days": 7, "wind_speed_unit": "kmh", "precipitation_unit": "mm"
    }
    try:
        r = requests.get(base_url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None
