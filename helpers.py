# ------------------------------------ IMPORTS ------------------------------------
import streamlit as st



# ------------------------------------ HELPER FUNCTIONS ------------------------------------
def set_background():
    # Inject custom CSS to set the airspace background styling
    st.markdown("""
        <style>
        .black-background {
            background-color: black;
            position: fixed;
            top: 20px;
            left: 420px;
            right: 20px;
            bottom: 20px;
            overflow: hidden;
            border: 2px solid white;
        }
        </style>
        <div class="black-background">
        """, unsafe_allow_html=True
    )

def set_sidebar_width():
    # Inject custom CSS to set the width of the sidebar
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_airspace():
    # Inject custom CSS to set the airspace and aircraft styling
    airspace = """
    <style>
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    .black-background {
        background-color: black;
        position: fixed;
        top: 20px;
        left: 420px;
        right: 20px;
        bottom: 20px;
        overflow: hidden;
        border: 2px solid white;
    }
    .aircraft {
        color: white;
        position: absolute;
        font-size: 18px;
        transform: translate(-50%, -50%);
    }
    </style>
    <div class="black-background">
    """
    return airspace