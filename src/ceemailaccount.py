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

    def send_email(self, to_address, subject, body, cc_recipients=[]):
        """ Send a trial or pending email based on the club """

        # Build and send message
        msg = Message(
            account=self.account,
            folder=self.account.sent,
            subject=subject,
            body= HTMLBody(body),
            to_recipients=[Mailbox(email_address=to_address)],
            cc_recipients=[(Mailbox(email_address=x)) for x in cc_recipients]
        )

        msg.send_and_save()
        print("Message to {} sent.".format(to_address))
