import os

import blockcypher
import requests

from coinmarketcap import Market

BITCOIN_BALANCE_URL = "https://blockexplorer.com/api/addr"
ETHER_BALANCE_URL = "https://api.etherscan.io/api"

PHOTONS_TO_LITECOIN_MULTIPLIER = 10**8
WEI_TO_ETHER_MULTIPLIER = 10**18


COINS = {
    'BITCOIN': 'bitcoin',
    'ETHEREUM': 'ethereum',
    'LITECOIN': 'litecoin'
}

class Crypto(object):
    """
    This class takes in crypto addresses and provides functions for determing
    the balance and the USD amount in each wallet.

    Args:
        bitcoin_address (str): Bitcoin Address to scan
        ether_address (str): Bitcoin Address to scan
        litecoin_address (str): Bitcoin Address to scan

    Attributes:
        bitcoin_address (str): Bitcoin Address to scan
        ether_address (str): Bitcoin Address to scan
        litecoin_address (str): Bitcoin Address to scan
        bitcoin_url (str): URL to get a get request against to get bitcoin balance
        etherscan_api_key (str): API key for etherscan.io to get ether balance,
                                 determined by ETHERSCAN_API_KEY

    """
    def __init__(self, bitcoin_address, ether_address, litecoin_address):
        self.bitcoin_address = bitcoin_address
        self.ether_address = ether_address
        self.litecoin_address = litecoin_address


        self.bitcoin_url = "{host}/{address}".format(host=BITCOIN_BALANCE_URL, address=bitcoin_address)
        self.ether_url = ETHER_BALANCE_URL
        self.etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')

    def _get_bitcoin_balance(self):
        """
        Returns bitcoin balance of the class' bitcoin address

        Yields:
            bitcoin_balance: Bitcoin balance
        """

        response = requests.get(self.bitcoin_url)
        bitcoin_balance = response.json().get('balance')
        return float(bitcoin_balance)

    def _get_ether_balance(self):
        """
        Returns ether balance of the class' ether address

        Yields:
            ether_balance: Ether balance
        """
        response = requests.get(self.ether_url, params={'module': 'account',
                                                        'action': 'balance',
                                                        'address': self.ether_address,
                                                        'tag': 'latest',
                                                        'apikey': self.etherscan_api_key})
        ether_balance = float(response.json().get('result')) / WEI_TO_ETHER_MULTIPLIER
        return ether_balance

    def _get_litecoin_balance(self):
        """
        Returns litecoin balance of the class' litecoin address

        Yields:
            litecoin_balance: Litecoin balance
        """
        photon_balance = blockcypher.get_address_overview(self.litecoin_address, coin_symbol='ltc').get('balance')
        litecoin_balance = float(photon_balance) / PHOTONS_TO_LITECOIN_MULTIPLIER
        return litecoin_balance

    def _convert_to_usd(self, coin):
        """
        Returns USD representation of a coin's wallet balance

        Args:
            coin (str): Coin to get address balance of
        Yields:
            litecoin_balance: Litecoin balance
        """
        market = Market()

        if coin is COINS['BITCOIN']:
            bitcoin_price_usd = market.ticker(coin, convert='USD')[0].get('price_usd')
            return float(bitcoin_price_usd) * self._get_bitcoin_balance()
        elif coin is COINS['ETHEREUM']:
            ethereum_price_usd = market.ticker(coin, convert='USD')[0].get('price_usd')
            return float(ethereum_price_usd) * self._get_ether_balance()
        elif coin is COINS['LITECOIN']:
            litecoin_price_usd = market.ticker(coin, convert='USD')[0].get('price_usd')
            return float(litecoin_price_usd) * self._get_litecoin_balance()
        else:
            raise Exception('Coin "{coin}" not supported'.format(coin=coin))

    def get_bitcoin_in_usd(self):
        """
        Get balance of the class' bitcoin balance in USD
        """
        return self._convert_to_usd(COINS['BITCOIN'])

    def get_ether_in_usd(self):
        """
        Get balance of the class' ether balance in USD
        """
        return self._convert_to_usd(COINS['ETHEREUM'])

    def get_litecoin_in_usd(self):
        """
        Get balance of the class' litecoin balance in USD
        """
        return self._convert_to_usd(COINS['LITECOIN'])
