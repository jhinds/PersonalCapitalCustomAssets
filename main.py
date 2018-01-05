
BITCOIN_ADDRESS = os.getenv('BITCOIN_ADDRESS')
ETHER_ADDRESS = os.getenv('ETHER_ADDRESS')
LITECOIN_ADDRESS = os.getenv('LITECOIN_ADDRESS')

crypto = Crypto(bitcoin_address=BITCOIN_ADDRESS,
                ether_address=ETHER_ADDRESS,
                litecoin_address=LITECOIN_ADDRESS)
