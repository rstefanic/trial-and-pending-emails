from exchangelib import Account, Configuration, DELEGATE, Mailbox, Message, ServiceAccount
from getpass import getpass
import datetime
import os
import sys

TRIAL_EMAIL = os.path.join(os.path.abspath('.'), 'trial.html')
PENDING_EMAIL = os.path.join(os.path.abspath('.'), 'pending.html')
PENDING_TRIAL = "pending-trial-accounts({:%m-%d-%Y}).txt".format(datetime.datetime.now())
PENDING_TRIAL_REPORT = os.path.join(os.path.abspath('.'), PENDING_TRIAL)

class CEEmailAccount(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.credentials = ServiceAccount(
            username=self.username,
            password=self.password)
        self.config = Configuration(
            server='webmail.sherweb2010.com',
            credentials=self.credentials)
        self.account = Account(
            primary_smtp_address=self.username,
            config=self.config,
            autodiscover=False,
            access_type=DELEGATE)


    def show_inbox_count(self):
        return self.account.inbox.total_count

"""
addr = ''
msg = Message(
    account=this.account,
    folder=account.sent,
    subject='Test Email',
    body='Test Body for email',
    to_recipients=[Mailbox(email_address=addr)]
    )

msg.send_and_save()
print("Done.")
"""

def main():
    username = input("Username: ")
    password = getpass("Password: ")
    print("Connecting...")
    email_account = CEEmailAccount(username, password)
    print("\nLook for clubs with an expiration date of {:%m-%d-%Y} or earlier.\n"
          .format(datetime.datetime.now() + datetime.timedelta(days=14)))
    print(email_account.show_inbox_count())

if __name__ == '__main__':
    main()
