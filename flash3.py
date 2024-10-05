import csv
import random
import urllib.request
# from PIL import Image
# from io import BytesIO
import streamlit as st

# Import the other modular components (including the updated handle_groups)
import handle_groups
import oblivion
# import db_url
import local_choices

options = [
    "image+name",
    "flash_forgotten",
    "flash_all_names"
]

null_image = 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'

verbose = False

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

    # Step 1: Use the db_url.main() function to get the URL
    if 'spreadsheet_url' not in st.session_state:
        if url == "":
            # Allow the user to input the URL manually if it's not passed as an argument
            spreadsheet_url = st.text_input("Enter the database URL", "")
        else:
            spreadsheet_url = url

        if st.button("Submit URL"):
            if spreadsheet_url:
                st.session_state['spreadsheet_url'] = spreadsheet_url
            else:
                st.warning("Please enter a valid database URL to continue.")
                return  # Stop execution until a valid URL is entered

    # Ensure we have the URL before proceeding to Step 2
    if 'spreadsheet_url' in st.session_state:

        if verbose:
            st.write(f"Database URL: {st.session_state['spreadsheet_url']}")

        # Step 2: Mode selection using Streamlit's selectbox
        if 'selected_option' not in st.session_state:
            selected_option = st.selectbox("Choose a mode", options)

            if st.button("Submit Mode"):
                st.session_state['selected_option'] = selected_option

        # Ensure we have the mode selected before proceeding
        if 'selected_option' in st.session_state:

            if verbose:
                st.write(f"You selected: {st.session_state['selected_option']}")

            # Step 3: Load and process the flashcards after mode selection
            if 'flashcards_loaded' not in st.session_state:
                flashcards = load_flashcards_from_google_sheet(st.session_state['spreadsheet_url'], verbose=verbose)
                filtered_cards = handle_groups.main(flashcards, verbose=verbose)

                # Save the filtered flashcards to the session state to avoid reloading
                st.session_state['filtered_cards'] = filtered_cards
                st.session_state['flashcards_loaded'] = True

            # Step 4: Perform additional actions only after loading flashcards
            if st.session_state['flashcards_loaded']:
                filtered_cards = st.session_state['filtered_cards']

                # Handle forgotten cards mode
                if st.session_state['selected_option'] == options[1]:
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
                    show_flashcard(filtered_cards, st.session_state['selected_option'], current_index)
                else:
                    st.write("Congratulations! You've gone through all the flashcards.")

    # Clear oblivion and local_choices
    oblivion.cleanup_temp_csv()
    local_choices.cleanup_temp_txt()




if __name__ == "__main__":
    main()
