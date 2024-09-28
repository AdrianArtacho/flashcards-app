import streamlit as st
import string_split
import local_choices

def main(data, verbose=False):
    # Get the number of items in the list
    num_items = len(data)
    st.write(f"There is a total of {num_items} people in the list.")

    # Create an empty set to store unique 'group' values
    unique_groups = set()

    # Iterate through the list of dictionaries and add unique 'group' values to the set
    for item in data:
        raw_group_string = item['group']
        if verbose:
            st.write(f"Raw group string: {raw_group_string}")
        
        splitted_list = string_split.main(raw_group_string)
        if verbose:
            st.write(f"Splitted group list: {splitted_list}")

        for label in splitted_list:
            unique_groups.add(label)

    # Convert the set of unique 'group' values back to a list
    unique_groups_list = list(unique_groups)

    # Load preselected options from the local storage (if any)
    preselection = local_choices.load_list_from_txt()

    # Streamlit's multiselect widget for group selection
    selected_options = st.multiselect(
        "Select groups to filter flashcards:",
        unique_groups_list,
        default=preselection
    )

    # Save the selected options locally
    local_choices.save_list_to_txt(selected_options)

    if verbose:
        st.write(f"Selected options: {selected_options}")

    # Check if "ALL" was selected, if so, select all groups
    if "ALL" in selected_options or len(selected_options) == 0:
        st.write(f"Showing all {len(unique_groups_list)} groups!")
        selected_options = unique_groups_list

    if verbose:
        st.write(f"Final selected options: {selected_options}")

    # Filter the data based on selected groups
    filtered_data = [
        item for item in data 
        if any(word in selected_options for word in item['group'].split())
    ]

    if verbose:
        st.write(f"Filtered data: {filtered_data}")

    return filtered_data


if __name__ == "__main__":
    # Example data for testing
    data = [
        {'name': 'Person1', 'group': 'Elementar', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'},
        {'name': 'Person2', 'group': 'unclassified', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'},
        {'name': 'Person3', 'group': 'Elementar', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'},
        {'name': 'Person4', 'group': 'Leitung', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'},
        {'name': 'Person5', 'group': 'Elementar', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683'}
    ]
    filtered_data = main(data, verbose=True)
