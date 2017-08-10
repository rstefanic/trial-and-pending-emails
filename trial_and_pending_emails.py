from exchangelib import Account, Configuration, DELEGATE, HTMLBody, \
                        Mailbox, Message, ServiceAccount
from EmailSettings import EmailSettings

import datetime
import json
import os
import sys

PENDING_CLUBS = []
TRIAL_CLUBS = []

TRIAL_EMAIL = os.path.join(os.path.abspath('.'), 'trial.html')
PENDING_EMAIL = os.path.join(os.path.abspath('.'), 'pending.html')
PENDING_TRIAL = "pending-trial-accounts({:%m-%d-%Y}).txt".format(datetime.datetime.now())
PENDING_TRIAL_REPORT = os.path.join(os.path.abspath('.'), PENDING_TRIAL)

class CEEmailAccount(object):

    def __init__(self, username, password, smtp_address, server):
        self.username = username
        self.password = password
        self.credentials = ServiceAccount(
            username=self.username,
            password=self.password)
        self.config = Configuration(
            server=server, #'webmail.sherweb2010.com',
            credentials=self.credentials)
        self.account = Account(
            primary_smtp_address=smtp_address,
            config=self.config,
            autodiscover=False,
            access_type=DELEGATE)


    def show_inbox_count(self):
        return self.account.inbox.total_count

    def send_email(self, trial, admin_name, to_address):

        # Construct body of message
        body = "Dear {}".format(admin_name)
        if trial:
            with open(TRIAL_EMAIL) as file:
                body = ''.join(file.readlines())
        else:
            with open(PENDING_EMAIL) as file:
                body = ''.join(file.readlines())

        # Build and send message
        msg = Message(
            account=this.account,
            folder=account.sent,
            subject='Test Email',
            body= HTMLBody(body),
            to_recipients=[Mailbox(email_address=to_address)]
        )

        msg.send_and_save()
        print("Message to {} sent.".format(admin_name))

class Club(object):

    def __init__(self):
        self.club_name = input("Club name: ").strip()
        self.club_id = input("Club ID: ").strip()
        self.email = input("Email: ").strip()
        self.admin_name = input("Admin name: ").strip()
        trial = input("Trial Account [Y/n]: ").lower()

        if trial == 'n':
            self.trial = False
        else:
            self.trial = True

            
def main():
    email_settings = EmailSettings()
    print("Connecting...")
    email_account = CEEmailAccount(email_settings.username,
                                   email_settings.password,
                                   email_settings.smtp_address,
                                   email_settings.server)
                   
#   print("\nLook for clubs with an expiration date of {:%m-%d-%Y} or earlier.\n"
#          .format(datetime.datetime.now() + datetime.timedelta(days=14)))
    print(email_account.show_inbox_count())


if __name__ == '__main__':
    main()
