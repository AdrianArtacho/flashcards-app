import csv
import os

oblivion_filename = 'oblivion.csv'


def add_name_to_csv(name, filename=oblivion_filename, verbose=False):
    """
    Adds a name to the oblivion CSV if it does not already exist.
    """
    fieldnames = ['name']  # Assuming 'name' is the only field in the CSV

    # Check if name already exists in the CSV
    if name in read_csv_names(filename, verbose):
        if verbose:
            print(f"Name '{name}' already exists in '{filename}'.")
        return

    # Open the CSV file in append mode
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the name to the CSV
        writer.writerow({'name': name})

    if verbose:
        print(f"Name '{name}' added successfully to '{filename}'.")


def read_csv_names(filename=oblivion_filename, verbose=False):
    """
    Reads names from the oblivion CSV and returns them as a set.
    """
    if verbose:
        print(f"Reading from filename: {filename}")

    names = set()
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if verbose:
                    print(f"Row: {row}")
                names.add(row['name'])
    except FileNotFoundError:
        pass  # File doesn't exist initially, so return empty set

    if verbose:
        print(f"Names read: {names}")
    return names


def remove_name_from_csv(name, filename=oblivion_filename, verbose=False):
    """
    Removes a name from the oblivion CSV.
    """
    fieldnames = ['name']  # Assuming 'name' is the only field in the CSV

    # Read current names from CSV
    current_names = read_csv_names(filename, verbose)

    # Check if name exists in the CSV
    if name not in current_names:
        if verbose:
            print(f"Name '{name}' not found in '{filename}'.")
        return

    # Open the CSV file and create a temporary file to write updated contents
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile, \
         open(filename + '.tmp', 'w', newline='', encoding='utf-8') as tmpfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(tmpfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write rows except the one with the name to be removed
        for row in reader:
            if row['name'] != name:
                writer.writerow(row)

    # Replace the original file with the updated temporary file
    os.replace(filename + '.tmp', filename)

    if verbose:
        print(f"Name '{name}' removed successfully from '{filename}'.")


def filter_forgotten_cards(filtered_cards, filename=oblivion_filename, verbose=False):
    """
    Filters the list of flashcards to only include those in the oblivion CSV.
    If no names from the CSV match, return the original list.
    """
    backup_list = filtered_cards
    oblivion_names = read_csv_names(filename, verbose)

    if verbose:
        print(f"Oblivion names: {oblivion_names}")

    # Filter the cards based on names in oblivion.csv
    filtered_cards = [card for card in filtered_cards if card['name'] in oblivion_names]

    if len(filtered_cards) == 0:
        if verbose:
            print("No names in the oblivion list, starting anew with the original list.")
        return backup_list

    if verbose:
        print(f"Filtered cards count: {len(filtered_cards)}")
    return filtered_cards
