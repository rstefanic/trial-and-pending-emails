from getpass import getpass
from json import load

class EmailSettings(object):

    def __init__(self):
        
        with open("config.json") as config:
            config_file = load(config)

        try:
            self.username = config_file['username']

            if self.username == "":
                raise ValueError("Empty username")
            
        except (KeyError, ValueError):
            self.username = input("Username: ")

        try:
            self.password = config_file['password']

            if self.password == "":
                raise ValueError("Empty password")
            
        except (KeyError, ValueError):
            self.password = getpass("Password: ")

        try:
            self.smtp_address = config_file['smtp_address']

            if self.smtp_address == "":
                raise ValueError("Defaulting SMTP Address")
            
        except (KeyError, ValueError):
            self.smtp_address = self.username

        try:
            self.server = config_file['server']

            if self.server == "":
                raise ValueError("Defaulting server to webmail.sherweb2010.com")
            
        except (KeyError, ValueError):
            self.server = 'webmail.sherweb2010.com'
