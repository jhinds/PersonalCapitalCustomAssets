import os
from src.crypto import Crypto
from src.personal_capital import PersonalCap

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

BITCOIN_ADDRESS = os.getenv('BITCOIN_ADDRESS')
ETHER_ADDRESS = os.getenv('ETHER_ADDRESS')
LITECOIN_ADDRESS = os.getenv('LITECOIN_ADDRESS')
PC_USERNAME = os.getenv('PC_USERNAME')
PC_PASSWORD = os.getenv('PC_PASSWORD')
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

crypto = Crypto(bitcoin_address=BITCOIN_ADDRESS,
                ether_address=ETHER_ADDRESS,
                litecoin_address=LITECOIN_ADDRESS)


p_cap = PersonalCap(pc_username=PC_USERNAME,
                            pc_password=PC_PASSWORD,
                            email_username=EMAIL_USERNAME,
                            email_password=EMAIL_PASSWORD)
