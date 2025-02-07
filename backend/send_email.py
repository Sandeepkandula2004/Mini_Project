from flask import Flask, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail for Outlook SMTP
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # For Outlook
app.config['MAIL_PORT'] = 587  # Port for TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '22341A4217@gmrit.edu.in'
app.config['MAIL_PASSWORD'] = 'sandeep@12345'  # Outlook account password
app.config['MAIL_DEFAULT_SENDER'] = '22341A4217@gmrit.edu.in'

# Initialize Flask-Mail
mail = Mail(app)

def get_unique_ids():
    """
    This function returns a list of unique email IDs.
    Modify it to retrieve the IDs as per your application's requirements.
    """
    return ["22341A4217"]

@app.route('/', methods=['GET'])
def send_bulk_emails():
    try:
        # Get email subject and body from the request
        subject = request.form.get('subject', 'Default Subject')
        body = request.form.get('body', 'This is a test email.')

        # Retrieve the list of unique email IDs
        recipient_emails = get_unique_ids()

        # Loop through each email and send it
        for recipient in recipient_emails:
            _ = f"{recipient}@gmrit.edu.in"
            print(_)
            msg = Message(subject, recipients=[_], body=body)
            mail.send(msg)
        
        return f"Emails sent successfully to {len(recipient_emails)} recipients!"
    except Exception as e:
        return f"Failed to send emails. Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
