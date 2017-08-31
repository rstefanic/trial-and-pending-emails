from src.emailsettings import EmailSettings
from src.ceemailaccount import CEEmailAccount
import src.generatereports as GR

import datetime
import json
import os
import sys

""" Constants and classes """

# Lists used to store clubs
PENDING_CLUBS = []
TRIAL_CLUBS = []

# Dates used
CURRENT_DATE = "{:%m-%d-%Y}".format(datetime.datetime.now())
FOURTEEN_DAYS_FROM_NOW = "{:%m-%d-%Y}".format(datetime.datetime.now() +
                                             datetime.timedelta(days=14))

# Paths for files used and created
TRIAL_EMAIL = os.path.join(os.path.abspath('./src'), 'trial.txt')
PENDING_EMAIL = os.path.join(os.path.abspath('./src'), 'pending.txt')
PENDING_TRIAL = "pending-trial-accounts({}).txt".format(CURRENT_DATE)
PENDING_TRIAL_REPORT = os.path.join(os.path.abspath('.'), PENDING_TRIAL)

# Data Types

class Club(object):
    """ Club Information """

    def __init__(self):
        self.club_name = input("Club name: ").strip()
        self.club_id = input("Club ID: ").strip()
        self.email = input("Email: ").strip()
        self.admin_name = input("Admin name: ").strip()
        self.body = "Dear {},".format(self.admin_name) 
        trial = input("Trial Account [Y/n]: ").lower()
        if trial == 'n'or trial == 'no':
            self.trial = False
            self.subject = "Pending Account Notice"
            with open(PENDING_EMAIL) as file:
                self.body += ''.join(file.readlines())
        else:
            self.trial = True
            self.subject = "Trial Account Notice"
            with open(TRIAL_EMAIL) as file:
                self.body += ''.join(file.readlines())

# To add a club to the PENDING_CLUBS or TRIAL_CLUBS list
def add_to_list(club, ls):
    return ls.append(club)    

""" Program Flow """

# Used to loop through and create Clubs and send an email to them.
def email_club_admins(email, settings):
    """ Main Loop: loop through until all the admins have been emailed """
    
    print("\nLook for clubs with an expiration date of {} or earlier.\n"
          .format(FOURTEEN_DAYS_FROM_NOW))

    while True:
        print("\n")
        club = Club()
        email.send_email(club.email, club.subject, club.body)
        if club.trial == False:
            add_to_list(club, PENDING_CLUBS)
        else:
            add_to_list(club, TRIAL_CLUBS)

        user_input = input("Would you like to add another? [Y/n] >> ")
        if user_input == 'n':
            break

# Email the report summary
def email_report(email_account, to_address, cc_recipients, subject, message):
    user_input = input("Would you like to email a report? [Y/n] >> ").lower()
    if user_input != 'n':
        email_account.send_email(to_address, subject, message, cc_recipients)

# Main
def main():
    email_settings = EmailSettings()
    print(email_settings.to_address)
    print(email_settings.cc_recipients)
    print("Connecting...")
    email_account = CEEmailAccount(email_settings.username,
                                   email_settings.password,
                                   email_settings.smtp_address,
                                   email_settings.server)
    print("Connected to {}".format(email_settings.server))

    email_club_admins(email_account, email_settings)
    report = GR.write_report(PENDING_TRIAL_REPORT, PENDING_CLUBS, TRIAL_CLUBS, verbose=True)
    email_report(email_account, email_settings.to_address, email_settings.cc_recipients,
                 "Pending and Trial Accounts ({})".format(CURRENT_DATE),
                 GR.generate_summary(PENDING_CLUBS, TRIAL_CLUBS,
                                     GR.print_short_info, html=True))
    sys.exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()
