import csv
csv_columns = ['No','Фамилия','Место/проживания']
dict_data = [
{'No': 1, 'Фамилия': 'Alex', 'Место/проживания': 'India'},
{'No': 2,  'Место/проживания': 'USA', 'Фамилия': 'Ben' },
]
csv_file = "Names.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
except IOError:
    print("I/O error") 