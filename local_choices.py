import os
import tempfile
import streamlit as st

# Create a temporary file when the session starts and store the filename in Streamlit's session state
def create_temp_txt():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w+', encoding='utf-8')
    temp_file.close()  # Close the file so we can access it later
    return temp_file.name

# Initialize the session state with the temporary file if not already set
if 'local_choices_filename' not in st.session_state:
    st.session_state['local_choices_filename'] = create_temp_txt()

# Save a list to the temporary text file
def save_list_to_txt(lst, filename=st.session_state['local_choices_filename'], verbose=True):
    """
    Saves a list to a temporary text file stored in the session state.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for item in lst:
            f.write(f"{item}\n")

    if verbose:
        print(f"List saved to '{filename}' successfully:", lst)
    else:
        print(f"List saved to '{filename}' successfully.")


# Load a list from the temporary text file
def load_list_from_txt(filename=st.session_state['local_choices_filename'], verbose=False):
    """
    Loads a list from the temporary text file stored in the session state.
    """
    lst = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                lst.append(line.strip())  # Remove newline characters and add to the list
    except FileNotFoundError:
        if verbose:
            print(f"File '{filename}' not found, returning an empty list.")
        return []

    if verbose:
        print(f"List loaded from '{filename}' successfully.")
    
    return lst


# Optional cleanup: Delete the temp file when needed (can be triggered at the end of the session)
def cleanup_temp_txt():
    if 'local_choices_filename' in st.session_state:
        os.remove(st.session_state['local_choices_filename'])
        del st.session_state['local_choices_filename']
