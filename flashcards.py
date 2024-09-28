import csv
import random
import urllib.request
from PIL import Image
from io import BytesIO
import streamlit as st

# Import the other modular components (including the updated handle_groups)
import handle_groups
import oblivion
import db_url

options = [
    "image+name",
    "flash_forgotten",
    "flash_all_names"
]

null_image = 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'

def load_flashcards_from_google_sheet(spreadsheet_url, verbose=False):
    flashcards = []
    response = urllib.request.urlopen(spreadsheet_url)
    tsv_data = response.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(tsv_data, delimiter='\t')

    for row in csv_reader:
        name, group, image_url, person_info = row
        flashcards.append({'name': name, 'group': group, 'image_url': image_url, 'info': person_info})

    return flashcards

def show_flashcard(flashcards, selected_option, current_index):
    flashcard = flashcards[current_index]
    name = flashcard['name']
    image_url = flashcard['image_url']

    # Create columns for buttons and image layout
    col1, col2, col3 = st.columns([1, 4, 1])  # Thin columns on sides, wide column in the center

    # Left column (Remove from flashcards)
    with col1:
        if st.button('❌', key=f"{name}_removed"):
            oblivion.remove_name_from_csv(name, verbose=False)
            st.session_state['current_index'] += 1  # Move to the next flashcard

    # Center column (Image and optional text)
    with col2:
        if image_url == null_image:
            st.write(f"↑↑↑ No image for {name} ↑↑↑")
            oblivion.remove_name_from_csv(name, verbose=False)
        else:
            if selected_option == options[0]:  # Show image and name
                st.image(image_url, caption=name, use_column_width=True)
                st.write(flashcard['info'])
            else:  # Just show the image
                st.image(image_url, caption=name, use_column_width=True)

    # Right column (Mark as remembered)
    with col3:
        if st.button('✅', key=f"{name}_remembered"):
            oblivion.add_name_to_csv(name, verbose=True)
            st.session_state['current_index'] += 1  # Move to the next flashcard


def main(url="", options=options, verbose=False):
    st.title("Flashcard Game")

    # Use the db_url.main() function to get the URL
    if url == "":
        spreadsheet_url = db_url.main(verbose=verbose)
    else:
        spreadsheet_url = url

    # Ensure a URL is entered before proceeding
    if not spreadsheet_url:
        st.warning("Please enter a valid database URL to continue.")
        return  # Stop execution until a valid URL is entered

    # Mode selection using Streamlit's selectbox
    selected_option = st.selectbox("Choose a mode", options)

    # Only proceed if a mode is selected
    if selected_option:
        st.write(f"You selected: {selected_option}")

        # Load flashcards from the Google Sheets URL
        flashcards = load_flashcards_from_google_sheet(spreadsheet_url, verbose=verbose)

        # Filter flashcards based on group selection using the updated handle_groups
        filtered_cards = handle_groups.main(flashcards, verbose=verbose)

        # If the user selects "flash_forgotten", filter forgotten cards
        if selected_option == options[1]:
            filtered_cards = oblivion.filter_forgotten_cards(filtered_cards)

        # Shuffle the flashcards for random display
        random.shuffle(filtered_cards)

        # Initialize the session state for flashcard index
        if 'current_index' not in st.session_state:
            st.session_state['current_index'] = 0

        # Display flashcards one by one
        current_index = st.session_state['current_index']

        # If there are still flashcards left to show
        if current_index < len(filtered_cards):
            show_flashcard(filtered_cards, selected_option, current_index)
        else:
            st.write("Congratulations! You've gone through all the flashcards.")


if __name__ == "__main__":
    main()
