import email, getpass, imaplib, os, re

from personalcapital import PersonalCapital as PersonalCapitalClient
from personalcapital import TwoFactorVerificationModeEnum

TWOFA_CODE_REGEX = '4-Digit Authorization Code:\d*([^\n\r]\d.{1,3})'

class PersonalCap(object):
    def __init__(self, pc_username, pc_password, email_username, email_password):
        self.client = PersonalCapitalClient()

        self.pc_username = pc_username
        self.pc_password = pc_password
        self.email_username = email_username
        self.email_password = email_password

    def _login(self):
        try:
            self.client.login(username=self.pc_username, password=self.pc_password)
        except:
            self.client.two_factor_challenge(TwoFactorVerificationModeEnum.EMAIL)

            ## get 2FA code magic via SMS or email tbd.
            code = self._get_code_from_email()

            self.client.two_factor_authenticate(TwoFactorVerificationModeEnum.EMAIL, code)
            self.client.authenticate_password(self.pc_password)

    def _get_code_from_email(self):
        mailbox = imaplib.IMAP4_SSL("imap.gmail.com")
        mailbox.login(self.email_username, self.email_password)
        mailbox.select('inbox')
        result, data = mailbox.search(None, "ALL")
        mail_ids = data[0] # data is a list.
        mail_ids_list = mail_ids.split() # ids is a space separated string
        latest_email_id = mail_ids_list[-1] # get the latest
        result, data = mailbox.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        raw_email = str(data[0][1])


        code = re.search(TWOFA_CODE_REGEX, raw_email)[1].split()[0]
        return code
