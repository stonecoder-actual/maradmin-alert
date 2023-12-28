import csv

def read_names_from_csv(csv_file):
    names = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')  # Specify tab as the delimiter
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            names.append((first_name.lower(), last_name.lower()))
    return names

csv_file_path = 'contacts.csv'
friends_names = read_names_from_csv(csv_file_path)
print(friends_names)