import streamlit as st
from utils.utils import update_page_state


def main(team): 
    with team.container():
        update_page_state("team")

        st.write("""<br><center><h2>Meet the Team</h2></center><br>""", unsafe_allow_html=True)

        a,b,c = st.columns([1,3,1])
        
        with b.container(border=True):
            st.write("<br>" * 2, unsafe_allow_html=True)
            cols = st.columns([0.5,2,2,2,0.5])
            for col in cols[1:4]:
                with col:
                    st.write(
                        f"<center><p>{'John Doe<br>'*10}</p></center>",
                        unsafe_allow_html=True,
                    )
            st.write("<br>" * 2, unsafe_allow_html=True)