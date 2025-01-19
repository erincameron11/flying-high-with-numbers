# =====================>TESTING
# if "x" not in st.session_state:
#     st.session_state.x = random.randint(10, 90)  # Starting x position (10-90%)
# if "y" not in st.session_state:
#     st.session_state.y = random.randint(10, 90)  # Starting y position (10-90%)
# if "dx" not in st.session_state:
#     st.session_state.dx = random.choice([-1, 1])  # Initial x direction (-1 or 1)
# if "dy" not in st.session_state:
#     st.session_state.dy = random.choice([-1, 1])  # Initial y direction (-1 or 1)

# # Function to update the position and direction of the text
# def update_position():
#     # Update position
#     st.session_state.x += st.session_state.dx
#     st.session_state.y += st.session_state.dy

#     # Handle boundary collisions
#     if st.session_state.x <= 0 or st.session_state.x >= 100:
#         st.session_state.dx *= -1  # Reverse direction on x-axis
#     if st.session_state.y <= 0 or st.session_state.y >= 100:
#         st.session_state.dy *= -1  # Reverse direction on y-axis

# # Display the moving text
# st.markdown(
#     f"""
#     <style>
#     .black-background {{
#         background-color: black;
#         height: 100vh;
#         width: 100vw;
#         position: relative;
#     }}
#     .aircraft {{
#         color: white;
#         position: absolute;
#         font-size: 24px;
#         transform: translate(-50%, -50%);
#     }}
#     </style>
#     <div class="black-background">
#         <div class="aircraft" style="top: {st.session_state.y}%; left: {st.session_state.x}%; ">
#             AC1234
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # Update position and rerun the app periodically
# time.sleep(0.05)  # Adjust the speed of movement
# update_position()
# st.rerun()





    


# ------------------------------------ IMPORTS ------------------------------------
import streamlit as st
import random
import time
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io


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
    
    # ---SIDEBAR---
    st.sidebar.title(":airplane: Flying High with Numbers")
    st.sidebar.divider()
    aircraft_nums = st.sidebar.text_input(
        "Aircraft numbers (separated by a comma): "
    )
    speed = st.sidebar.slider("Speed", min_value=1.0, max_value=10.0, value=1., step=0.25)
    start = st.sidebar.button("Start", use_container_width=True)
    pause = st.sidebar.button("Pause", use_container_width=True)
    
    # Define canvas dimensions
    WIDTH = 800
    HEIGHT = 450

    
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
                "x": [random.randint(30, WIDTH - 30) for _ in range(len(aircraft))],
                "y": [random.randint(30, HEIGHT - 30) for _ in range(len(aircraft))],
                "dx": [random.choice([-1, 1]) * speed for _ in range(len(aircraft))],
                "dy": [random.choice([-1, 1]) * speed for _ in range(len(aircraft))],
            })
    if pause:
        st.session_state.paused = True

    
    # Create a container to update the image
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
            st.session_state.aircraft_data["x"] += st.session_state.aircraft_data["dx"]
            st.session_state.aircraft_data["y"] += st.session_state.aircraft_data["dy"]
    
            # Boundaries for each aircraft
            for i in range(len(st.session_state.aircraft_data)):
                # Minus 25 to account for right boundary edge
                if st.session_state.aircraft_data.loc[i, "x"] <= 0 or st.session_state.aircraft_data.loc[i, "x"] >= WIDTH - 25:
                    st.session_state.aircraft_data.loc[i, "dx"] *= -1
                # Minus 20 to account for lower boundary edge
                if st.session_state.aircraft_data.loc[i, "y"] <= 0 or st.session_state.aircraft_data.loc[i, "y"] >= HEIGHT - 20:
                    st.session_state.aircraft_data.loc[i, "dy"] *= -1
    
        # Create a black background for the canvas 
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
        # Draw the aircraft numbers
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)


        # ---STYLING---
        # Try using Arial font, and if it doesn't work, use the default
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

        # Colour the aircraft names with white text and use the specified font
        for i in range(len(st.session_state.aircraft_data)):
            draw.text((st.session_state.aircraft_data.loc[i, "x"], st.session_state.aircraft_data.loc[i, "y"]),
                      st.session_state.aircraft_data.loc[i, "aircraft"], fill="white", font=font)

        img = np.array(pil_img)        
    
        # Show the airspace radar
        airspace_container.image(img, channels="BGR", use_column_width=True)
    
        # Pause for animation speed
        time.sleep(1 / 40)
        st.rerun()


# ------------------------------------ RUN THE APP ------------------------------------
if __name__ == "__main__":
    main()