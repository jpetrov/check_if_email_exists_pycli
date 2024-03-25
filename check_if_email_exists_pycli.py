import csv
import subprocess
import sys
import re
import os

def extract_is_reachable_value(output):
    pattern = r'"is_reachable":\s*"([^"]+)",'
    match = re.search(pattern, output)
    if match:
        value = match.group(1)
        return value  # Return the extracted value
    else:
        return "Error"

if __name__ == "__main__":
    # Check if the required arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python check.py input_file.csv output_file.csv")
        sys.exit(1)

    email_column_index = 4
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Open the input CSV file
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Open the output CSV file
        with open(output_file, 'w', newline='') as output_file:
            fieldnames = csv_reader.fieldnames + ['is_reachable']
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            # Iterate over each row in the input CSV
            for row in csv_reader:
                # Get the cell value from the desired column
                cell_value = row[csv_reader.fieldnames[email_column_index]]

                # Run the external CLI command and capture its output
                check_email_command = f"{os.path.expanduser('~')}/Source/check-if-email-exists/target/release/check.sh {cell_value}"
                result = subprocess.run(check_email_command, shell=True, capture_output=True, text=True)

                # Extract the "is_reachable" value from the output
                is_reachable_value = extract_is_reachable_value(result.stdout)

                # Add the extracted value to the row
                row['is_reachable'] = is_reachable_value

                # Write the modified row to the output CSV
                csv_writer.writerow(row)
