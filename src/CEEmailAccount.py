from exchangelib import Account, Configuration, DELEGATE, HTMLBody, \
                        Mailbox, Message, ServiceAccount

class CEEmailAccount(object):
    """ Establish connection to email account """

    def __init__(self, username, password, smtp_address, server):
        self.username = username
        self.password = password
        self.credentials = ServiceAccount(
            username=self.username,
            password=self.password)
        self.config = Configuration(
            server=server,
            credentials=self.credentials)
        self.account = Account(
            primary_smtp_address=smtp_address,
            config=self.config,
            autodiscover=False,
            access_type=DELEGATE)


    def show_inbox_count(self):
        return self.account.inbox.total_count

    def send_email(self, trial, admin_name, to_address):
        """ Send a trial or pending email based on the club """
        
        # Construct body of message
        body = "Dear {}".format(admin_name)
        if trial:
            subject = "Trial Account Notice"
            with open(TRIAL_EMAIL) as file:
                body = ''.join(file.readlines())
        else:
            subject = "Pending Account Notice"
            with open(PENDING_EMAIL) as file:
                body = ''.join(file.readlines())

        # Build and send message
        msg = Message(
            account=self.account,
            folder=self.account.sent,
            subject=subject,
            body= HTMLBody(body),
            to_recipients=[Mailbox(email_address=to_address)]
        )

        msg.send_and_save()
        print("Message to {} sent.".format(admin_name))
