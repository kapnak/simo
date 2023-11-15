import logging
import math
from binance.spot import Spot

from .exchange import Exchange
from .safe_operators import *


class Binance(Exchange):
    def __init__(self, api_key, api_secret):
        super().__init__()
        logging.info(f'Initialize new binance client with key : {api_key}.')
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Spot(self.api_key, self.api_secret)
        self.symbol_stable = 'FDUSD'
        self.symbol_bitcoin = 'BTC'
        self.symbol_pair = 'BTCFDUSD'
        self._price_tick_size = 100   # Tick size of BTCFDUSD 0.01000000
        self._lot_step_size = 100000  # Step size of BTCFDUSD 0.00010000

    def buy_max_market(self) -> float:
        order = self.client.new_order(symbol=self.symbol_pair,
                                      side='BUY',
                                      type='MARKET',
                                      quoteOrderQty=self.get_balance(self.asset_stable))
        if order['status'] != 'FILLED':
            logging.error(f'The market order status is not filled as expected. Status : {order["status"]}, order : {order}.')
            raise 'Order not filled : ' + order
        quantity = .0
        commission = .0
        for fill in order['fills']:
            quantity = add(quantity, fill['qty'])
            commission = add(commission, fill['commission'])
        total = substract(quantity, commission)
        logging.info(f'Bought {total} BTC ({quantity} - {commission} fees)')
        if commission > 0:
            logging.warning(f'Commissions are not null : {commission} !')
        return total

    def sell_max_limit(self, price: float):
        """
        Place a sell limit order.
        :param price: The bitcoin price.
        """
        self.client.new_order(symbol=self.symbol_pair,
                              side='SELL',
                              type='LIMIT',
                              price=float_to_str(divide(math.trunc(price * self._price_tick_size), self._price_tick_size)),
                              quantity=float_to_str(divide(math.trunc(self.get_balance(self.asset_bitcoin) * self._lot_step_size), self._lot_step_size)),
                              timeInForce='GTC')

    def get_open_price(self) -> float:
        """
        Get the last 1H candle open price.
        :return: The last 1H candle open price.
        """
        open_price = float(self.client.klines(symbol=self.symbol_pair, interval='1h', limit=1)[0][1])
        logging.info(f'Open price is {open_price}')
        return open_price

    def cancel_orders(self):
        """
        Cancel all orders on bitcoin.
        """
        # Issues with :
        # self.client.cancel_open_orders(symbol=self.symbol_pair)
        orders = self.client.get_open_orders(symbol=self.symbol_pair)
        for order in orders:
            self.client.cancel_order(symbol=self.symbol_pair, orderId=order['orderId'])

    def get_balance(self, balance_type: str) -> float:
        if balance_type is self.asset_stable:
            balance = float(self.client.user_asset(asset=self.symbol_stable)[0]['free'])
        elif balance_type is self.asset_bitcoin:
            balance = float(self.client.user_asset(asset=self.symbol_bitcoin)[0]['free'])
        else:
            total_bitcoin_valuation = add(
                self.client.user_asset(asset=self.symbol_bitcoin, needBtcValuation=True)[0]['btcValuation'],
                self.client.user_asset(asset=self.symbol_stable, needBtcValuation=True)[0]['btcValuation']
            )

            if balance_type is self.assets_bitcoin_valuation:
                balance = total_bitcoin_valuation
            elif balance_type is self.assets_stable_valuation:
                balance = multiply(total_bitcoin_valuation, self.client.ticker_price(self.symbol_pair)['price'])
            else:
                balance = None

        logging.info(f'Balance {balance_type} = {balance}')
        return balance
