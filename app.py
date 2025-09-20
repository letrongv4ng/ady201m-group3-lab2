import streamlit as st
from src.api import get_coordinates_from_city, fetch_weather_data
from src.transform import process_weather_data
from src.charts import render_metric_tabs
import pandas as pd

st.set_page_config(page_title="Group 3", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'>EasyWeather</h1>
    <h3 style='text-align: center;'>Present by group [3]: Le Hung, Quang Minh and Manh Chung</h3>
    """,
    unsafe_allow_html=True
)


st.header("Input Options")
col1, col2 = st.columns(2)

with col1:
    input_type = st.radio("Choose input method:", ["City Name", "Coordinates"])
    if input_type == "City Name":
        city_input = st.text_input("Enter city name:", value="Hanoi", placeholder="e.g., Hanoi, Vietnam")
        latitude = longitude = None
    else:
        latitude = st.number_input("Latitude:", value=21.0285, format="%.4f")
        longitude = st.number_input("Longitude:", value=105.8542, format="%.4f")
        city_input = None

with col2:
    metrics = st.multiselect("Select metrics to display:", ["Temperature","Precipitation","Wind"], default=[])

if st.button("Fetch Weather Data", type="primary"):
    if not metrics:
        st.error("Please select at least one metric to display.")
    else:
        # get coords
        if input_type == "City Name" and city_input:
            with st.spinner("Getting coordinates..."):
                lat, lon, found = get_coordinates_from_city(city_input)
                if lat is None:
                    st.error(f"Could not find coordinates for '{city_input}'.")
                    st.stop()
                latitude, longitude = lat, lon
                st.success(f"Found: {found} ({lat:.4f}, {lon:.4f})")
                st.info(f"Using city name: {city_input}")

        if latitude is None or longitude is None:
            st.error("Please provide valid coordinates or city name.")
            st.stop()

        # fetch → transform
        with st.spinner("Fetching weather data..."):
            data = fetch_weather_data(latitude, longitude, metrics)
            df = process_weather_data(data, metrics) # type: ignore

        if df is None or df.empty:
            st.error("No data received.")
        else:
            st.success("Weather data fetched successfully!")
            st.header("Weather Forecast Data")
            st.dataframe(df, use_container_width=True)

            st.header("Weather Forecast Charts")
            render_metric_tabs(df, metrics)

            st.info(f"Location: {latitude:.4f}, {longitude:.4f}")
            st.info(f"Timezone: {data.get('timezone', 'Unknown') if data else 'Unknown'}")

            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                               "forecast.csv", "text/csv")
