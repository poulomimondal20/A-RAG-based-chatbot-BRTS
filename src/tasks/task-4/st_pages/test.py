import streamlit as st
import pydeck as pdk


# Configure your map setup here
def map_config(landmark_color="#ff0000"):
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[
            {"position": [77.1025, 28.7041], "size": 100}  # Example coordinates
        ],
        get_position="position",
        get_color=landmark_color,
        get_radius="size",
    )
    view_state = pdk.ViewState(
        latitude=28.7041,
        longitude=77.1025,
        zoom=10,
        pitch=45,
    )
    tooltip = {"html": "<b>Location:</b> {position}"}
    return layer, view_state, tooltip


st.title("Rotatable BRTS Map")

# Mapbox style and view config
MAPBOX_STYLES = {
    "light": "mapbox://styles/mapbox/light-v9",
    "dark": "mapbox://styles/mapbox/dark-v9",
}

mapbox_style = "light"

with st.container():
    # Add a slider to control the bearing of the map
    bearing = st.slider("Map Rotation", min_value=0, max_value=360, step=1, value=0)

    layer, view_state, tooltip = map_config(landmark_color="#ff0000")

    # Update view_state bearing for rotation
    view_state.bearing = bearing

    brts_map = pdk.Deck(
        map_style=MAPBOX_STYLES[mapbox_style],
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip,
    )
    st.pydeck_chart(brts_map)
