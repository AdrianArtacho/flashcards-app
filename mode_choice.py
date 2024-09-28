def main(options, verbose=False):
    # options = [
    #     "image+name",
    #     "flash_images",
    #     "flash_names"
    # ]
    
    print("Choose an option:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    choice = input("Enter the number of your choice: ")
    
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(options):
            selected_option = options[index]
            if verbose:
                print(f"You chose: {selected_option}")
            
            # Perform actions based on the selected option
            # if selected_option == options[1]:
            #     # Perform action for image+name option
            #     print("Performing action for image+name...")
            # elif selected_option == options[2]:
            #     # Perform action for flash_images option
            #     print("Performing action for flash_images...")
            # elif selected_option == options[3]:
            #     # Perform action for flash_names option
            #     # print("Performing action for flash_names...")
            return selected_option
        else:
            print("Invalid choice. Please enter a valid number.")
    else:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
