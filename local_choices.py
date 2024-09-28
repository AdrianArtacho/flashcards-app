local_choices_filename = 'local_choices.txt'

def save_list_to_txt(lst, filename=local_choices_filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(f"{item}\n")

# Example list
# my_list = ['apple', 'banana', 'cherry', 'date']
# filename = 'my_list.txt'

# Save the list to a .txt file
# save_list_to_txt(my_list, filename)

    print(f"List saved to '{filename}' successfully.")


def load_list_from_txt(filename=local_choices_filename, verbose=False):
    lst = []
    with open(filename, 'r') as f:
        for line in f:
            # Remove newline characters and add to the list
            lst.append(line.strip())
    
    if verbose:
        print("List loaded from file:")
        print(filename)
    
    return lst

# File from which to load the list
# filename = 'my_list.txt'

# # Load the list from the .txt file
# loaded_list = load_list_from_txt(filename)

# print("List loaded from file:")
# print(filename)
