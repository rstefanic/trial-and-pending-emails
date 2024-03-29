from getpass import getpass
from json import load

import sys

class EmailSettings(object):
    """ Create an object with all connection settings """

    def __init__(self):

        with open("config.json") as config:
            config_file = load(config)

        # Get username safely
        try:
            self.username = config_file['username']

            if self.username == "":
                raise ValueError("Empty username")
            
        except (KeyError, ValueError):
            self.username = input("Username: ")

        # Get password safely
        try:
            self.password = config_file['password']

            if self.password == "":
                raise ValueError("Empty password")
            
        except (KeyError, ValueError):
            self.password = getpass("Password: ")

        # Get SMTP address safely
        try:
            self.smtp_address = config_file['smtp_address']

            if self.smtp_address == "":
                raise ValueError("Defaulting SMTP Address")
            
        except (KeyError, ValueError):
            self.smtp_address = self.username

        # Get server safely
        try:
            self.server = config_file['server']

            if self.server == "":
                raise ValueError("Defaulting server to webmail.sherweb2010.com")
            
        except (KeyError, ValueError):
            self.server = 'webmail.sherweb2010.com'


        # Get Primary to email address safely
        try:
            self.to_address = config_file['primary_to_address']

        except (KeyError, ValueError):
            self.to_address = None
            

        # Get CC recpients safely
        try:
            self.cc_recipients = config_file['cc_recipients']

        except (KeyError, ValueError):
            self.cc_recipients = []
