from personalcapital import PersonalCapital as PersonalCapitalClient

class PersonalCap(object):
    def __init__(self, username, password):
        self.client = PersonalCapitalClient()

        self.username = username
        self.password = password

    def _login(self):
        try:
            self.client(username=self.username, password=self.password)
        except:
            self.client(username=self.username, password=self.password)
            self.client.two_factor_challenge(mode)

            ## get 2FA code magic via SMS or GMAIL tbd
            self.client.two_factor_authenticate(mode, raw_input('code'))

            self.client.authenticate_password(self.password)
