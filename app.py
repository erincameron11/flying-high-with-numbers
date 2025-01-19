# ------------------------------------ IMPORTS ------------------------------------
import streamlit as st
import random
import time
import pandas as pd
import numpy as np
# Import external files
from helpers import *


# ------------------------------------ MAIN APP ------------------------------------
def main():
    """
    Main method to run the application.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """   
    # Change the title and favicon of the app in the browser
    st.set_page_config(layout="wide", page_title='Flying High', page_icon=":airplane:")

    set_background()
    
    # ---SIDEBAR---
    set_sidebar_width() # from helpers.py
    st.sidebar.title(":airplane: Flying High with Numbers")
    st.sidebar.divider()
    aircraft_nums = st.sidebar.text_input(
        "Aircraft numbers (separated by a comma): "
    )
    speed = st.sidebar.slider("Speed", min_value=1, max_value=60, value=10, step=1)
    start = st.sidebar.button("Start", use_container_width=True)
    pause = st.sidebar.button("Pause", use_container_width=True)
    reset = st.sidebar.button("Reset", use_container_width=True)

    
    # ---STATES---
    if "aircraft_data" not in st.session_state:
        st.session_state.aircraft_data = pd.DataFrame(columns=["aircraft", "x", "y", "dx", "dy"])
    if "running" not in st.session_state:
        st.session_state.running = False
    if "paused" not in st.session_state:
        st.session_state.paused = False

    
    # ---BUTTONS---
    if start:
        st.session_state.running = True
        st.session_state.paused = False
        # Generate new aircraft data if none currently exists
        if st.session_state.aircraft_data.empty and aircraft_nums:
            # Obtain each separate aircraft number
            aircraft = [s.strip() for s in aircraft_nums.split(',')]
            # Position the aircraft x, y coordinates and dx, dy on the canvas
            st.session_state.aircraft_data = pd.DataFrame({
                "aircraft": aircraft,
                "x": [random.randint(10, 90) for _ in range(len(aircraft))],
                "y": [random.randint(10, 90) for _ in range(len(aircraft))],
                "dx": [random.choice([-1, 1]) * speed for _ in range(len(aircraft))],
                "dy": [random.choice([-1, 1]) * speed for _ in range(len(aircraft))],
            })
    if pause:
        st.session_state.paused = True

    if reset:
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.aircraft_data = pd.DataFrame(columns=["aircraft", "x", "y", "dx", "dy"])
        st.session_state.aircraft_nums = ''

    
    # Create a container to update the airspace display
    airspace_container = st.empty()

    
    # ---ANIMATION LOOP---
    # While the app is running
    while st.session_state.running:
        if not st.session_state.paused:
            # Dynamically adjust the speed
            for i in range(len(st.session_state.aircraft_data)):
                st.session_state.aircraft_data.loc[i, "dx"] = (
                    speed if st.session_state.aircraft_data.loc[i, "dx"] > 0 else -speed
                )
                st.session_state.aircraft_data.loc[i, "dy"] = (
                    speed if st.session_state.aircraft_data.loc[i, "dy"] > 0 else -speed
                )
    
            # Update positions of each aircraft
            st.session_state.aircraft_data["x"] += st.session_state.aircraft_data["dx"] * 0.01
            st.session_state.aircraft_data["y"] += st.session_state.aircraft_data["dy"] * 0.01
    
            # Boundaries collision checker for each aircraft
            for i in range(len(st.session_state.aircraft_data)):
                if st.session_state.aircraft_data.loc[i, "x"] <= 2 or st.session_state.aircraft_data.loc[i, "x"] >= 98:
                    st.session_state.aircraft_data.loc[i, "dx"] *= -1
                if st.session_state.aircraft_data.loc[i, "y"] <= 8 or st.session_state.aircraft_data.loc[i, "y"] >= 98:
                    st.session_state.aircraft_data.loc[i, "dy"] *= -1

        # Render the airspace
        airspace_html = render_airspace()
        for _, row in st.session_state.aircraft_data.iterrows():
            airspace_html += f'<div class="aircraft" style="top: {row["y"]}%; left: {row["x"]}%">{row["aircraft"]}</div>'
        airspace_html += "</div>"

        airspace_container.markdown(airspace_html, unsafe_allow_html=True)
    
        # Pause for animation speed
        time.sleep(1 / 40)
        st.rerun()


# ------------------------------------ RUN THE APP ------------------------------------
if __name__ == "__main__":
    main()