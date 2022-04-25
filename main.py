import imaplib
import email
from email.header import decode_header
from decouple import config

# Account Credentials
username = config("USERNAME")
password = config("PASSWORD")

mail_server = "imap.gmail.com"

# Create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(mail_server)

# Authentication
imap.login(username, password)

# Selecting mailbox to work with
imap.select("inbox")


user_response = (
    input("Do you wish to search by subject or by sender? (type: subject or sender) ")
    .lower()
    .strip()
)

if user_response == "sender":
    sender = input("Enter the sender mail address: ").lower().strip()
    status, messages = imap.search(None, f"FROM {sender}")
    messages = messages[0].split(b" ")
    # Loop to iterate over targeted mails and mark them as deleted
    for mail in messages:
        _, msg = imap.fetch(mail, "(RFC822)")
        # This second loop is only for printing the SUBJECT of targeted mails
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Decoding the mail subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # If it is a bytes type, decode to str
                    subject = subject.decode()
                print("Deleting", subject)
        # Marking the mail as deleted
        imap.store(mail, "+FLAGS", "\\Deleted")


elif user_response == "subject":
    subject = input("Enter the subject key-words: ").lower().strip()
    status, messages = imap.search(None, f"SUBJECT {subject}")
    messages = messages[0].split(b" ")
    # Loop to iterate over targeted mails and mark them as deleted
    for mail in messages:
        _, msg = imap.fetch(mail, "(RFC822)")
        # This second loop is only for printing the SUBJECT of targeted mails
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # Decoding the mail subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # If it is a bytes type, decode to str
                    subject = subject.decode()
                print("Deleting", subject)
        # Marking the mail as deleted
        imap.store(mail, "+FLAGS", "\\Deleted")

# Else statement to prevent error in caso neither of the other two statemets are true (should i use try and except?)
else: 
    imap.close()


imap.expunge()
imap.close()
imap.logout()