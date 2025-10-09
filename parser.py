import os
import email
import csv
from email.policy import default

# Define the path to the maildir directory
maildir_path = 'maildir'
# Define the name of the output CSV file
output_csv_file = 'emails.csv'

def parse_email(file_path):
    """Parses a single email file and extracts its content."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            msg = email.message_from_file(f, policy=default)
        
        # Safely get headers
        from_ = msg.get('From', 'N/A')
        to_ = msg.get('To', 'N/A')
        subject_ = msg.get('Subject', 'N/A')
        
        # Get the email body
        body = 'N/A'
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # Skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                    break
        else:
            # Not a multipart message, get the payload (body) directly
            body = msg.get_payload(decode=True).decode('utf-8', 'ignore')
            
        return from_, to_, subject_, body

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None, None, None, None

# --- Main Script ---
print("Starting email parsing process...")

# Prepare the CSV file
with open(output_csv_file, 'w', newline='', encoding='utf--8') as f:
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(['From', 'To', 'Subject', 'Body'])

    email_count = 0
    # Walk through the maildir directory
    for root, dirs, files in os.walk(maildir_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Parse the email and get the data
            from_addr, to_addr, subject, body_text = parse_email(file_path)
            
            # Write to CSV only if the data is valid
            if from_addr and to_addr:
                writer.writerow([from_addr, to_addr, subject, body_text])
                email_count += 1
                
                # Print a progress update every 1000 emails
                if email_count % 1000 == 0:
                    print(f"Processed {email_count} emails...")

print(f"\nParsing complete. Processed a total of {email_count} emails.")
print(f"Data saved to {output_csv_file}")