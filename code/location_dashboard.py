import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Set page config
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_locations():
    return pd.read_csv('./cache/top_locations.csv')

@st.cache_data
def load_tickets():
    return pd.read_csv('./cache/tickets_in_top_locations.csv')

top_locs = load_locations()
tickets_df = load_tickets()

# Dashboard title
st.title("Parking Ticket Analysis by Location")

# Location selection
selected_loc = st.selectbox(
    "Select a location:",
    options=top_locs.sort_values('location')['location']
)

# Filter data for selected location
loc_tickets = tickets_df[tickets_df['location'] == selected_loc]
loc_data = top_locs[top_locs['location'] == selected_loc]

# Create columns for layout
col1, col2 = st.columns(2)

with col1:
    # Metrics
    st.metric("Total Tickets", len(loc_tickets))
    st.metric("Total Fines", f"${loc_data['amount'].values[0]:,.2f}")

    # Day of week chart
    st.subheader("Tickets by Day of Week")
    day_counts = loc_tickets['dayofweek'].value_counts().sort_index()
    fig_day = px.bar(
        day_counts,
        labels={'value': 'Number of Tickets', 'index': 'Day of Week'},
        title=f"Tickets by Day at {selected_loc}"
    )
    st.plotly_chart(fig_day, use_container_width=True)

with col2:
    # Hour of day chart
    st.subheader("Tickets by Hour of Day")
    hour_counts = loc_tickets['hourofday'].value_counts().sort_index()
    fig_hour = px.line(
        hour_counts,
        labels={'value': 'Number of Tickets', 'index': 'Hour of Day'},
        title=f"Tickets by Hour at {selected_loc}"
    )
    st.plotly_chart(fig_hour, use_container_width=True)

    # Map
    st.subheader("Location Map")
    if not loc_data.empty:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": loc_tickets['lat'].iloc[0],
                "longitude": loc_tickets['lon'].iloc[0],
                "zoom": 16,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=loc_data,
                    get_position=['lon', 'lat'],
                    get_radius=100,
                    get_fill_color=[255, 0, 0, 200],
                    pickable=True
                )
            ],
            tooltip={
                "html": "<b>Selected Location:</b> {location}",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }
        ))