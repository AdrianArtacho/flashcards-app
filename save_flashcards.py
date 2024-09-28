import csv

csv_filename = 'flashcards.csv'

def main(data, csv_filename=csv_filename):
    # Specify the field names for the CSV file
    fieldnames = ['name', 'group', 'image_url', 'info']

    # exit()

    # Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write the data rows
        for item in data:
            writer.writerow(item)

    print(f'CSV file "{csv_filename}" has been created successfully.')

if __name__ == "__main__":
    data = [
        {'name': 'Person A', 'group': 'Elementar', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683', 'info': 'whatever'},
        {'name': 'Person B', 'group': 'unclassified', 'image_url': 'https://docs.google.com/drawings/d/e/2PACX-1vQmT77hMdDIKbK0PIgXorXv5awKMOHNr_XS6nczlWcGENot_LYyC_mqtG_1KpRmIZPgKdKNhT62Rcru/pub?w=684&h=683', 'info': 'whatever'}
    ]
    main(data)