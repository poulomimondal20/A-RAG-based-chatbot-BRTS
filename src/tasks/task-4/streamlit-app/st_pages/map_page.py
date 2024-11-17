import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_js_eval import get_geolocation

from utils.chatbot import ask_question
from utils.constants import LANDMARK_COLORS, MAPBOX_STYLES, AVATAR
from utils.utils2 import find_nearest_station_by_time, get_osrm_distance_and_time, display_current_info, update_page_state


og_df = pd.read_csv("assets/data/all_routes_combined.csv")
df = og_df.copy()

df["size"] = 5
df["color"] = df.apply(lambda x: LANDMARK_COLORS[x["route"]]["rgb"], axis=1)


def user_selected_map(user_current_location_info, closet_bus_station):
    arc_data = []
    scatter_data = []
    # df = df[df['route'] == selected_route] if selected_route != 'All' else df

    # for i in range(len(df) - 1):
    arc_data.append(
        {
            "from_name": user_current_location_info["station"],
            "to_name": closet_bus_station["station"],
            "from_coordinates": [
                user_current_location_info["longitude"],
                user_current_location_info["latitude"],
            ],
            "to_coordinates": [
                closet_bus_station["longitude"],
                closet_bus_station["latitude"],
            ],
            "route": closet_bus_station["route"],
        }
    )

    scatter_data.append(
        {
            "coordinates": [
                closet_bus_station["longitude"],
                closet_bus_station["latitude"],
            ],
            "station_name": closet_bus_station["station"],
        }
    )

    scatter_data.append(
        {
            "coordinates": [
                user_current_location_info["longitude"],
                user_current_location_info["latitude"],
            ],
            "station_name": user_current_location_info["station"],
        }
    )

    arc_layer = pdk.Layer(
        "ArcLayer",
        arc_data,
        pickable=True,
        get_source_position="from_coordinates",
        get_target_position="to_coordinates",
        # get_source_color=LANDMARK_COLORS[selected_route]['source'],
        # get_target_color=LANDMARK_COLORS[selected_route]['target'],
        get_width=3,
        auto_highlight=True,
        tooltip={"text": "{from_name} to {to_name} - Route: {route}"},
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        scatter_data,
        pickable=True,
        get_position="coordinates",
        # get_fill_color=LANDMARK_COLORS[selected_route]['rgb'],
        get_radius=100,
        tooltip={"text": "{station_name}"},
    )

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=11,
        bearing=0,
        pitch=50,
    )

    r = pdk.Deck(
        layers=[arc_layer, scatter_layer],
        initial_view_state=view_state,
    )

    return r


def map_config(df, user_lat=None, user_long=None):
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position="[longitude, latitude]",
        get_radius=50,
        get_color="color",
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=user_lat if user_lat else df["latitude"].mean(),
        longitude=user_long if user_long else df["longitude"].mean(),
        zoom=14 if user_lat and user_long else 10,
        pitch=50,
    )

    tooltip = {"html": "<b>Station:</b> {station}", "style": {"color": "white"}}

    return layer, view_state, tooltip

def main(map_):
    global df, og_df

    with map_.container():
        update_page_state("map")
        cols = st.columns([1, 2.5, 1.2])

        with cols[0]:
            with st.container(border=True):
                st.write('<h4 class="poppins-light">Dashboard</h4>', unsafe_allow_html=True)
                locate_me = st.checkbox("Locate Me", key="locate_me")
                mapbox_style = st.selectbox(
                    "Map Style", [i.title() for i in MAPBOX_STYLES], key="mapbox_style"
                )

                user_lat, user_long = None, None
                nearest_station = None
                nearest_station_coords = None

                if locate_me:
                    loc = get_geolocation()  # Get location only if "Locate Me" is checked
                    if loc is not None:
                        st.toast("📍 Locating you...")
                        user_lat, user_long = (
                            loc["coords"]["latitude"],
                            loc["coords"]["longitude"],
                        )
                        st.toast(f"📍 Location found! {user_lat}, {user_long}")

                        # Add the user's location as an additional point to the map
                        additional_point = pd.DataFrame(
                            {
                                "station": ["Your Location"],
                                "latitude": [user_lat],
                                "longitude": [user_long],
                                "color": [[255, 255, 255]],  # White color for user location
                                "size": [20],  # Size of the point on the map
                            }
                        )
                        df = pd.concat([df, additional_point])

                        # Only display current information once the location is fetched
                        with st.container(border=True, height=260):
                            st.write('<h4 class="poppins-light">Info</h4>', unsafe_allow_html=True)
                            display_current_info_ = display_current_info(df=og_df, user_lat=user_lat, user_long=user_long)

                            # Show a message that we're finding the nearest stop
                            with st.spinner("Finding nearest stop..."):
                                nearest_station, best_distance, shortest_time = find_nearest_station_by_time(user_lat, user_long)
                                if nearest_station:
                                    st.write(f"Nearest station: {nearest_station} <br>(Distance: {best_distance} meters, Time: {shortest_time} seconds)", unsafe_allow_html=True)
                                    nearest_station_coords = (df.loc[df['station'] == nearest_station, 'latitude'].values[0], df.loc[df['station'] == nearest_station, 'longitude'].values[0])
                                else:
                                    st.error("Could not find a nearby stop.")
                    else:
                        st.toast("📍 Location not found. Please try again.")  # Fallback message if location isn't found
                else:
                    # If "Locate Me" is not checked, ask the user to manually enter latitude and longitude
                    # st.write("📍 Enter Latitude and Longitude manually")
                    # user_lat = st.number_input("Latitude", format="%.6f", key="manual_lat")
                    # user_long = st.number_input("Longitude", format="%.6f", key="manual_lon")
                    
                    if user_lat and user_long:
                        st.write(f"Latitude: {user_lat}, Longitude: {user_long}")

                        # Add the manually entered location as an additional point to the map
                        additional_point = pd.DataFrame(
                            {
                                "station": ["Manual Location"],
                                "latitude": [user_lat],
                                "longitude": [user_long],
                                "color": [[0, 0, 255]],  # Blue color for manual location
                                "size": [20],  # Size of the point on the map
                            }
                        )
                        df = pd.concat([df, additional_point])

                        # Show a message that we're finding the nearest stop
                        with st.spinner("Finding nearest stop..."):
                            nearest_station, best_distance, shortest_time = find_nearest_station_by_time(user_lat, user_long)
                            if nearest_station:
                                st.success(f"Nearest station: {nearest_station} (Distance: {best_distance} meters, Time: {shortest_time} seconds)")
                                nearest_station_coords = (df.loc[df['station'] == nearest_station, 'latitude'].values[0], df.loc[df['station'] == nearest_station, 'longitude'].values[0])
                            else:
                                st.error("Could not find a nearby stop.")

                if nearest_station_coords:
                    lat, long = nearest_station_coords
                    # Generate a navigation link to Google Maps
                    navigation_link = f"https://www.google.com/maps/dir/{user_lat},{user_long}/{lat},{long}"
                    st.write(f"🛣️ [Get directions to nearest station](%s)" % navigation_link)

            if not locate_me:
                st.image(r"assets/img/omdena.png", use_container_width=True)

        with cols[1]:
            with st.container(border=True, height=530):
                if user_lat is not None and user_long is not None:
                    # Only show the map with the user's location if the location was successfully fetched
                    layer, view_state, tooltip = map_config(
                        df, user_lat=user_lat, user_long=user_long
                    )
                    brts_map = pdk.Deck(
                        map_style=MAPBOX_STYLES[mapbox_style.lower()],
                        initial_view_state=view_state,
                        layers=[layer],
                        tooltip=tooltip,
                    )
                    st.pydeck_chart(brts_map)
                else:
                    # Display the default map or message if "Locate Me" is not selected
                    layer, view_state, tooltip = map_config(df)
                    brts_map = pdk.Deck(
                        map_style=MAPBOX_STYLES[mapbox_style.lower()],
                        initial_view_state=view_state,
                        layers=[layer],
                        tooltip=tooltip,
                    )
                    st.pydeck_chart(brts_map)

        with cols[2]:
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {
                        "role": "assistant", 
                        "content": "I can help you with your queries about the BRTS System. How can I assist you today?"
                    }
                ]

            with st.container(border=True):
                st.write('<h4 class="poppins-light chatbot-heading">Chatbot</h4>', unsafe_allow_html=True)
                with st.container(border=False, height=385):
                    for msg in st.session_state.messages:
                        st.chat_message(msg["role"]).write(msg["content"])

                    m1 = st.empty()
                    m2 = st.empty()

                if prompt := st.chat_input():
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    m1.chat_message("user").write(prompt)
                    with st.spinner("Lemme think..."):
                        msg = ask_question(query=str(prompt), current_location=locate_me)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    m2.chat_message("assistant").write(msg)


if __name__ == "__main__":
    main()