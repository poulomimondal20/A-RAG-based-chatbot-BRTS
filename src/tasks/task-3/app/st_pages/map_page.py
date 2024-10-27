import humanize
import warnings
import pandas as pd
import pydeck as pdk
import streamlit as st
import plotly.express as px
from streamlit_js_eval import get_geolocation
from constants import LANDMARK_COLORS, MAPBOX_STYLES
from utils import hex_to_rgb

og_df = pd.read_csv("assets/data/all_routes_combined.csv")
df = og_df.copy()
df['size'] = 5

def map_config(landmark_color):
    layer = pdk.Layer(
        'ScatterplotLayer',
        df,
        get_position='[longitude, latitude]',
        get_radius=50,
        get_color=hex_to_rgb(landmark_color),
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=10,
        pitch=10
    )

    tooltip = {
        "html": "<b>Station:</b> {station}",
        "style": {"color": "white"}
    }
    
    return layer, view_state, tooltip


def main(map):
    global df
    
    # map.write("<h3>📊 Overview Of BRTS Dataset</h3>", unsafe_allow_html=True)
    a1, a2, a3, a4, input_area, locate_me = map.columns([0.65,0.65,0.65,1,1.6,0.5])

    try:
        # selected_route = input_area.selectbox("Select a Route", ['All', *LANDMARK_COLORS], key="selected_route")
        # csv = df.to_csv(index=False).encode('utf-8')

        # locate_me.write("<br>"*1, unsafe_allow_html=True)

        cols = map.columns([0.3,1])
        
        with cols[0]:
            # with st.container(border=True, height=530):
            with st.container():
                st.write('<h4 class="poppins-light">Dashboard</h4>', unsafe_allow_html=True)
                locate_me = st.checkbox("Locate Me", key="locate_me")
                mapbox_style = st.selectbox("Map Style", MAPBOX_STYLES, key="mapbox_style")
                # landmark_color = st.color_picker("Color", key="landmark_color", value="#ffff00")
                # st.write('<button class="my-button"><i class="fa-solid fa-rotate-right">&nbsp;&nbsp;</i>Reset</button>', unsafe_allow_html=True)
                st.info('more components to be added here')
                
                if locate_me:
                    loc = get_geolocation()
                    if loc is not None:
                        st.toast("📍 Locating you...")
                        user_lat, user_long = loc['coords']['latitude'], loc['coords']['longitude']
                        st.toast("📍 Location found! {} {}".format(user_lat, user_long))
                        additional_point = pd.DataFrame({
                            'latitude': user_lat,
                            'longitude': user_long,
                            'color': ['#00ff00'],
                            'size': [20]
                        })

                        df = pd.concat([df, additional_point])

                
        with cols[1]:
            layer, view_state, tooltip = map_config(landmark_color="#ff0000")
            map = pdk.Deck(
                        map_style=MAPBOX_STYLES[mapbox_style],
                        initial_view_state=view_state,
                        layers=[layer],
                        tooltip=tooltip,
                )
            st.pydeck_chart(map)
        
    except Exception as e:
        st.error(e)

if __name__ == '__main__':
    main()