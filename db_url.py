import streamlit as st

def main(verbose=False):
    # Use Streamlit's text input to prompt the user for a database URL
    if 'db_url' not in st.session_state:
        st.session_state.db_url = ""  # Initialize session state for the URL

    db_url = st.text_input("Please enter a database URL:", value=st.session_state.db_url)

    # Store the entered URL in session state
    st.session_state.db_url = db_url

    # If verbose is True, display the entered URL
    if verbose and db_url:
        st.write(f"You entered: {db_url}")

    return db_url
