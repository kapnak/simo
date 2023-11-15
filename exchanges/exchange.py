import logging
from abc import ABC, abstractmethod


class Exchange(ABC):
    def __init__(self):
        """
        Initialize exchange.
        """
        self.asset_bitcoin = 'bitcoin'
        self.asset_stable  = 'stable'
        self.assets_bitcoin_valuation = 'asset_bitcoin_valuation'
        self.assets_stable_valuation  = 'asset_stable_valuation'

    @abstractmethod
    def buy_max_market(self) -> float:
        """
        Buy Bitcoin in market using all the available stable coin.
        :return: The amount of bitcoin bought.
        """
        logging.info('Buy max market.')

    @abstractmethod
    def sell_max_limit(self, price: float):
        """
        Place a sell limit order.
        :param price: The bitcoin price.
        """
        logging.info(f'Placing a sell limit order at {price}.')

    @abstractmethod
    def get_open_price(self) -> float:
        """
        Get the last 1H candle open price.
        :return: The last 1H candle open price.
        """
        pass

    @abstractmethod
    def cancel_orders(self):
        """
        Cancel all orders on bitcoin.
        """
        logging.info(f'Cancelling all open orders on bitcoin.')

    @abstractmethod
    def get_balance(self, assets: str) -> float:
        """
        Get balance.
        :param assets: The asset type. (Exchange.assets['bitcoin' / 'stable' / 'total']
        :return: The balance.
        """
        pass
