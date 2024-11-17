import numpy as np
import streamlit as st
import pandas as pd
import requests
from utils.constants import FIRST_MESSAGE_TEMPLATE
from concurrent.futures import ThreadPoolExecutor, as_completed
from scipy.spatial import KDTree
from time import sleep
from requests.exceptions import RequestException
import math

# Constants
OSRM_URL = "https://ayush-003-bhopal-brts-osrm.hf.space/route/v1/driving/{},{};{},{}"
data_url = "https://dagshub.com/Omdena/VITBhopalUniversity_ChatbotforBRTSNavigation/raw/99c2e8d2883dd9faaa68ed60d5405dd40e77c456/src/tasks/task-2/Routes/all_routes_combined.csv"

# Load data
df = pd.read_csv(data_url)
latitude_column = 'Latitude'
longitude_column = 'Longitude'
name_column = 'Station'

# Pre-compute KDTree
coordinates = np.radians(df[[latitude_column, longitude_column]])
kdtree = KDTree(coordinates)

def get_osrm_distance_and_time(row, user_lat, user_lon,max_retries=5, timeout=5):
    stop_lat = row[latitude_column]
    stop_lon = row[longitude_column]
    url = OSRM_URL.format(user_lon, user_lat, stop_lon, stop_lat)
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params={'overview': 'false'}, timeout=timeout)
            if response.status_code == 200:
                osrm_data = response.json()
                return row[name_column], osrm_data['routes'][0]['distance'], osrm_data['routes'][0]['duration']
            else:
                print(f"OSRM error {response.status_code}: {response.text}")
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            sleep(2) 

def find_nearest_station_by_time(user_lat, user_lon, max_stops=10):
    # Convert user location to radians
    user_point = np.radians([user_lat, user_lon])

    # Step 1: Get nearest stations using KDTree
    dist, idx = kdtree.query(user_point, k=max_stops)  # Get nearest stations
    nearby_stops = df.iloc[idx]

    nearest_station = None
    shortest_time = float('inf')
    best_distance = None
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_osrm_distance_and_time, row, user_lat, user_lon): row for _, row in nearby_stops.iterrows()}
        for future in as_completed(futures):
            result = future.result()
            if result:
                station_name, distance, duration = result
                if duration < shortest_time:
                    shortest_time = duration
                    best_distance = distance
                    nearest_station = station_name

    return nearest_station, best_distance, shortest_time

def display_current_info(df, user_lat, user_long):
    try:
        # Get the nearest station based on travel time
        station_name, distance, duration = find_nearest_station_by_time(user_lat, user_long)

        if station_name:
            formatted_message = FIRST_MESSAGE_TEMPLATE.format(
                station=station_name,
                distance=round(distance / 1000, 2),  # Convert to km
                duration=round(duration / 60, 2)  # Convert to minutes
            )

            # Display station info
            st.write(formatted_message)
            st.link_button(
                "Navigate using Google Maps",
                url=f"https://www.google.com/maps/dir/{user_lat},{user_long}/{station_name}",
                use_container_width=True,
            )
            return station_name, formatted_message 

    except KeyError:
        pass
    except Exception as e:
        st.error(e)
        

def update_page_state(state):
    
    print(state)
    if "page_state" not in st.session_state:
        st.session_state["page_state"] = ""
    if "hide_scrollbar" not in st.session_state:
        st.session_state["hide_scrollbar"] = False
        
    page_state = st.session_state.page_state = state 
    # st.toast(page_state)
    return page_state

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
    print(hex_to_rgb("#ff0000"))
