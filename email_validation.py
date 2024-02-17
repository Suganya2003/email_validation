import csv
from tempfile import NamedTemporaryFile
import shutil
import mx
import smtp
import syntval
import tempdom


def label_email(email):
    if not syntval.is_valid_email(email):
        return "Invalid"
    if not mx.has_valid_mx_record(email.split('@')[1]):
        return "Invalid"
    if not smtp.verify_email(email):
        return "Unknown"
    if not tempdom.is_disposable(email.split('@')[1]):
        return "Risky"
    return "Valid"


def label_emails(input_file):
    validation_result = []  # Store the validation results
    with open(input_file, 'r') as csvfile, \
            NamedTemporaryFile(mode='w', delete=False) as temp_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_file)

        # Write the header row to the output file
        writer.writerow(['Email', 'Label'])

        # Process each row in the input file
        for row in reader:
            email = row[0].strip()
            label = label_email(email)
            writer.writerow([email, label])
            validation_result.append(label)  # Add validation result to the list

    # Calculate and display accuracy percentage
    calculate_accuracy(validation_result)

    # Replace the input file with the output file
    shutil.move(temp_file.name, 'Output file.csv')


def calculate_accuracy(validation_result):
    total_emails = len(validation_result)
    valid_emails = validation_result.count('Valid')
    invalid_emails = validation_result.count('Invalid')
    unknown_emails = validation_result.count('Unknown')
    risky_emails = validation_result.count('Risky')

    valid_percentage = (valid_emails / total_emails) * 100
    invalid_percentage = (invalid_emails / total_emails) * 100
    unknown_percentage = (unknown_emails / total_emails) * 100
    risky_percentage = (risky_emails / total_emails) * 100

    print(f"Accuracy Percentage:")
    print(f"Valid: {valid_percentage:.2f}%")
    print(f"Invalid: {invalid_percentage:.2f}%")
    print(f"Unknown: {unknown_percentage:.2f}%")
    print(f"Risky: {risky_percentage:.2f}%")


# Example usage:
label_emails('Email List.csv')

