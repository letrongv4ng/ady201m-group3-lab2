# src/charts.py
import plotly.graph_objects as go
import streamlit as st

GROUPS = {
    "Temperature": ["Max Temp (°C)", "Min Temp (°C)"],
    "Precipitation": ["Precipitation (mm)"],
    "Wind": ["Max Wind Speed (km/h)"],
}

def render_metric_tabs(df, metrics: list[str]):
    groups = {k: [c for c in GROUPS[k] if c in df.columns] for k in metrics if k in GROUPS}
    groups = {k: v for k, v in groups.items() if v}
    if not groups:
        st.info("No metrics to display.")
        return

    tabs = st.tabs(list(groups.keys()))
    for tab, title in zip(tabs, groups.keys()):
        with tab:
            cols = groups[title]
            fig = go.Figure()
            for col in cols:
                fig.add_trace(go.Scatter(x=df["Date"], y=df[col], mode="lines+markers", name=col))
            y_label = {"Temperature":"Temperature (°C)", "Precipitation":"Precipitation (mm)", "Wind":"Wind speed (km/h)"}[title]
            fig.update_layout(
                template="none", title={"text": title, "x":0.5},
                xaxis_title="Date", yaxis_title=y_label,
                plot_bgcolor="white", paper_bgcolor="white", height=480
            )
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("Show data"):
                st.dataframe(df[["Date"]+cols], use_container_width=True)
