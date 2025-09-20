# src/transform.py
import pandas as pd

COL_MAP = {
    "temperature_2m_max": "Max Temp (°C)",
    "temperature_2m_min": "Min Temp (°C)",
    "precipitation_sum": "Precipitation (mm)",
    "wind_speed_10m_max": "Max Wind Speed (km/h)",
}

def process_weather_data(data: dict, metrics: list[str]) -> pd.DataFrame | None:
    if not data or "daily" not in data:
        return None
    daily = data["daily"]
    df = pd.DataFrame({"Date": pd.to_datetime(daily["time"])})
    # chỉ add cột có trong JSON + user chọn
    for key, nice in COL_MAP.items():
        group = ("Temperature" if "Temp" in nice else
                 "Precipitation" if "Precipitation" in nice else
                 "Wind")
        if group in metrics and key in daily:
            df[nice] = daily[key]
    return df if not df.empty else None
