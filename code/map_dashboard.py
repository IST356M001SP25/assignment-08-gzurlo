import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page config
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('./cache/top_locations_mappable.csv')

data = load_data()

# Dashboard title
st.title("Syracuse Parking Ticket Hotspots")

# Calculate map view
midpoint = (data['lat'].mean(), data['lon'].mean())

# Create heatmap layer
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=data,
    get_position=['lon', 'lat'],
    get_weight='amount',
    radius_pixels=30,
    opacity=0.8,
)

# Create scatterplot layer for circles
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=['lon', 'lat'],
    get_radius="amount",
    radius_scale=0.01,
    get_fill_color=[255, 0, 0, 140],
    pickable=True
)

# Create tooltip
tooltip = {
    "html": "<b>Location:</b> {location}<br/><b>Total Fines:</b> ${amount:,.2f}",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# Create deck
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 12,
        "pitch": 50,
    },
    layers=[heatmap_layer, scatter_layer],
    tooltip=tooltip
))

# Show data table
st.subheader("Top Locations by Fine Amount")
st.dataframe(data.sort_values('amount', ascending=False))