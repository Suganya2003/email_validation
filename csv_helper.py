from tempfile import NamedTemporaryFile
import shutil
import csv
import email_validation


def label_emails(input_file, output_file):
    with open(input_file, 'r') as csvfile, \
            NamedTemporaryFile(mode='w', delete=False) as temp_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_file)

        # Write the header row to the output file
        writer.writerow(['Email', 'Label', 'Suggestions'])

        # Process each row in the input file
        for row in reader:
            email = row[0].strip()
            label = email_validation.label_email(email)

            # Get suggestions using the get_suggestions function from email_validation module
            suggestions = email_validation.get_suggestions(email)

            writer.writerow([email, label, suggestions])

    # Replace the input file with the output file
    shutil.move(temp_file.name, output_file)


label_emails('Email List1.csv')
