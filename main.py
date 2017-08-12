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

    email_club_admins(email_account)
    write_report(PENDING_TRIAL_REPORT, PENDING_CLUBS, TRIAL_CLUBS, verbose=True)
    

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

            
def email_club_admins(email):
    """ Main Loop: loop through until all the admins have been emailed """
    
    print("\nLook for clubs with an expiration date of {:%m-%d-%Y} or earlier.\n"
          .format(datetime.datetime.now() + datetime.timedelta(days=14)))

    while True:
        print("\n")
        club = Club()
        email.send_email(club.trial,
                         club.admin_name,
                         club.email,
                         TRIAL_EMAIL,
                         PENDING_EMAIL)
        if club.trial == False:
            add_to_list(club, PENDING_CLUBS)
        else:
            add_to_list(club, TRIAL_CLUBS)

        user_input = input("Would you like to add another? [Y/n] >> ")

        if user_input == 'n':
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()
