from src.EmailSettings import EmailSettings
from src.CEEmailAccount import CEEmailAccount
from src.GenerateReports import write_report

import datetime
import json
import os
import sys

PENDING_CLUBS = []
TRIAL_CLUBS = []

TRIAL_EMAIL = os.path.join(os.path.abspath('./src'), 'trial.html')
PENDING_EMAIL = os.path.join(os.path.abspath('./src'), 'pending.html')
PENDING_TRIAL = "pending-trial-accounts({:%m-%d-%Y}).txt".format(datetime.datetime.now())
PENDING_TRIAL_REPORT = os.path.join(os.path.abspath('.'), PENDING_TRIAL)

def main():
    email_settings = EmailSettings()
    print("Connecting...")
    email_account = CEEmailAccount(email_settings.username,
                                   email_settings.password,
                                   email_settings.smtp_address,
                                   email_settings.server)
    print("Connected to {}".format(email_settings.server))

def add_to_list(club, ls):
    return ls.append(club)

class Club(object):
    """ Store Club information """

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

    def __str__(self):
        return "- " + self.club_name + " (" + self.club_id + ")" + "\n\t\tAdmin: " + self.admin_name + " (" + self.email + ")"

            
def email_club_admins(email):
    """ Loop through until all the admins have been emailed """
    
    print("\nLook for clubs with an expiration date of {:%m-%d-%Y} or earlier.\n"
          .format(datetime.datetime.now() + datetime.timedelta(days=14)))

    while True:
        print("\n")
        club = Club()
        email.send_email(club.trial, club.admin_name, club_email)


if __name__ == '__main__':
    main()
