

csv_file = 'contacts.csv'
names = []
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        first_name = row['first_name']
        last_name = row['last_name']
        names.append((first_name.lower(), last_name.lower()))
print(names)