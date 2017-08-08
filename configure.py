"""

"""
from getpass import getpass
from json import load

def get_configuration():

    def safe_configuration_reading(field, sensitive=False):

        if sensitive == True:
            input_field = lambda: getpass("{}: ".format(field.title()))
        else:
            input_field = lambda: input("{}: ".format(field.title()))
            
        return_field = ""

        try:
            return_field = config_file[filed]
        except KeyError:
            print("ERROR: Could not read config file for '%s'".format(field))
            print("Please enter in your %s or exit and fix the config file.")
            return_field = input_field()
        finally:
            if return_field == "":
                return_field = input_field()

                return return_field

    with open("config.json") as config:
        config_file = load(config)

    username = safe_configuration_reading('username')
    password = safe_configuration_reading('password', sensitive=True)
    smtp_password = safe_configuration_reading('smtp_address')
    
    return username, password, smtp_address


            
