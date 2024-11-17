import time
import random
import numpy as np
import streamlit as st
from utils.constants import FIRST_MESSAGE_TEMPLATE


def haversine(lat1, lon1, lat2, lon2):
    if None not in (lat1, lon1, lat2, lon2):
        R = 6371.0  # radius of the Earth
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        distance = R * c
        return distance

    return None

def find_closest_bus_station(df, current_lat, current_lon):
    df["distance"] = df.apply(
        lambda row: haversine(
            current_lat, current_lon, row["latitude"], row["longitude"]
        ),
        axis=1,
    )
    closest_point = df.loc[df["distance"].idxmin()]
    closest_point = closest_point.to_dict()
    closest_point["dir_to_closest_point"] = (
        f"https://www.google.com/maps/dir/{current_lat},{current_lon}/{closest_point['latitude']},{closest_point['longitude']}"
    )

    closest_point["all_routes"] = list(
        df[df["station"] == closest_point["station"]]["route"].unique()
    )

    return closest_point

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    return list(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))

def custom_write(query):
    for word in query:
        yield word + " "
        time.sleep(random.uniform(0.06, 0.1))

def display_current_info(df, user_lat, user_long):
    try:
        closest_bus_station = find_closest_bus_station(df, user_lat, user_long)
        if closest_bus_station is not None:
            formatted_message = FIRST_MESSAGE_TEMPLATE.format(station=closest_bus_station["station"],distance=round(closest_bus_station["distance"], 2),routes=" ".join(closest_bus_station["all_routes"]))
            
            st.write(formatted_message)
            st.link_button(
                "Navigate using Google Map",
                url=closest_bus_station["dir_to_closest_point"],
                use_container_width=True,
            )
            return closest_bus_station, formatted_message 
    
    except KeyError:
        pass
    
    except Exception as e:
        st.error(e)

def stream_data(data):
    for word in data.split(" "):
        yield word + " "
        time.sleep(random.uniform(0.06, 0.1))

def update_page_state(state):
    
    print(state)
    if "page_state" not in st.session_state:
        st.session_state["page_state"] = ""
    if "hide_scrollbar" not in st.session_state:
        st.session_state["hide_scrollbar"] = False
        
    page_state = st.session_state.page_state = state 
    # st.toast(page_state)
    return page_state


if __name__ == "__main__":
    print(hex_to_rgb("#ff0000"))