# Email Sender
import os
import smtplib
import ssl
import mimetypes
import re
from email.message import EmailMessage
from dotenv import load_dotenv

def is_valid_email (email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    matched = re.match(pattern, email)
    return matched


def send_email(receiver_email, subject, body, html_body, attachment_path=None):
    
    load_dotenv()
    sender_email = os.getenv("SENDER_EMAIL")
    sender_name = os.getenv("SENDER_NAME")
    password = os.getenv("APP_PASSWORD")
    smtp_server_address = os.getenv("SMTP_SERVER_ADDRESS")
    

    smtp_port = int(os.getenv("SMTP_PORT", 465))

    if not all([sender_email, password, smtp_server_address]):
        print("Error: Please make sure SENDER_EMAIL, APP_PASSWORD, and SMTP_SERVER_ADDRESS are set in your .env file.")
        return

    msg = EmailMessage()
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)
    msg.add_alternative(html_body, subtype='html')

    if attachment_path:
        
        if not os.path.exists(attachment_path):
            print(f"Error: Attachment file not found at '{attachment_path}'")
            choice = input("Press any key to continue sending (or press Enter to skip):  ")
            if not choice:
                return
        else:

            mime_type, _ = mimetypes.guess_type(attachment_path)

            if mime_type is None:
                mime_type, mime_subtype = 'application', 'octet-stream'
            else:
                mime_type, mime_subtype = mime_type.split('/', 1)

            with open(attachment_path, 'rb') as file:
                msg.add_attachment(file.read(),
                                   maintype=mime_type,
                                   subtype=mime_subtype,
                                   filename=os.path.basename(attachment_path))
            print(f"Attachment '{os.path.basename(attachment_path)}' added.")


    context = ssl.create_default_context()

    print("Connecting to server and sending email...")
    try:
        
        with smtplib.SMTP_SSL(smtp_server_address, smtp_port, context=context) as server:
            
            server.login(sender_email, password)
            server.send_message(msg)
        
        print("\nEmail sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("\nAuthentication failed. Please check your email/password (App Password).")
    except smtplib.SMTPConnectError:
        print("\nConnection failed. Could not connect to the server.")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":

    receiver = input("Enter receiver's email address: ")
    while True:
        if is_valid_email(receiver) :
            break
        else:
            receiver = input("Error, Enter receiver's email address: ")

    email_subject = "Test Email from Python Script"
    email_body = """
    Hello Mekdad,

    This is an automated email sent from the Python script we built together.
    It's working!

    Best regards,
    Your Python Bot
    """

    html_template = ''
    
    with open ('email.html' , 'r+') as file :
        html_template = file.read()

    attachment_filepath = input("Enter the full path of the file to attach without (or press Enter to skip):  ")

    if not attachment_filepath:
        attachment_filepath = None


    formatted_html = html_template.format(recipient_name=receiver.split('@')[0])

    send_email(receiver, email_subject, email_body, formatted_html, attachment_filepath)

    send_email(
        receiver_email=receiver,
        subject=email_subject,
        body=email_body,
        html_body=formatted_html,
        attachment_path=attachment_filepath if attachment_filepath else None
    )
