import csv
def read_from_csv(file_name, column_index):
        column_arr = []
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            header_skipped = False
            for row in csv_reader:
                if not header_skipped:
                    header_skipped = True
                    continue  # Skip header row
                if len(row) > column_index:
                    value = float(row[column_index])  # Convert to float
                    rounded_value = round(value, 2)  # Round the value
                    column_arr.append(rounded_value)
        return column_arr
