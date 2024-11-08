# import humanize
# import warnings
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_js_eval import get_geolocation
# import plotly.express as px

from utils.chatbot import ask_question
from utils.constants import LANDMARK_COLORS, MAPBOX_STYLES, AVATAR
from utils.utils import stream_data, find_closest_bus_station, display_current_info, update_page_state


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
                # 'More components can be added here'

                user_lat, user_long = None, None

                if locate_me:
                    loc = get_geolocation()
                    if loc is not None:
                        st.toast("📍 Locating you...")
                        user_lat, user_long = (
                            loc["coords"]["latitude"],
                            loc["coords"]["longitude"],
                        )
                        st.toast(f"📍 Location found! {user_lat}, {user_long}")

                        additional_point = pd.DataFrame(
                            {
                                "station": ["Your Location"],
                                "latitude": [user_lat],
                                "longitude": [user_long],
                                "color": [[255, 255, 255]],
                                "size": [20],
                            }
                        )
                        df = pd.concat([df, additional_point])

            with st.container(border=True, height=260 if locate_me else 220):
                if locate_me:
                    st.write('<h4 class="poppins-light">Info</h4>', unsafe_allow_html=True)
                    display_current_info_ = display_current_info(df=og_df, user_lat=user_lat, user_long=user_long)
                else:
                    st.write('<h4 class="poppins-light">Info</h4>', unsafe_allow_html=True)
                    st.write(
                        "Launched in 2006, Bhopal BRTS aimed to serve central districts but was discontinued in December 2023 due to traffic issues. Dismantling began January 2024, replaced by a central road divider."
                    )
            
            if not locate_me:
                st.image(r"assets/img/omdena.png", use_container_width=True)
                    

        with cols[1]:
            with st.container(border=True, height=530):
                # if locate_me:
                #     closest_bus_station = find_closest_bus_station(og_df, user_lat, user_long)
                #     new_map = user_selected_map(user_current_location_info=additional_point, closet_bus_station=closest_bus_station)
                #     st.pydeck_chart(new_map)

                # else:
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