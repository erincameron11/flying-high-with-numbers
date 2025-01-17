# ------------------------------------ IMPORTS ------------------------------------
import streamlit as st # for UI


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
    st.set_page_config(page_title='Flying High', page_icon=":airplane:")

    
    
    # Using "with" notation
    # with st.sidebar:
    aircraft_nums = st.sidebar.text_input(
    "Aircraft numbers (separated by a comma): "
    )

    start = st.sidebar.button("Start", use_container_width=True)
    stop = st.sidebar.button("Stop", use_container_width=True)
    restart = st.sidebar.button("Restart", use_container_width=True)


    # App title
    st.title(":airplane: Flying High with Numbers")
    st.divider()
    
    




# ------------------------------------ RUN THE APP ------------------------------------
if __name__ == "__main__":
    main()