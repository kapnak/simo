import os
import time
import logging
from threading import Thread
from datetime import datetime

import exchanges
from exchanges import safe_operators

USER_DIR = 'data/user/'
HN = 1.0025


def start(name):
    Thread(name=name, target=run, args=(name,)).start()


def start_all():
    for file in os.scandir(USER_DIR):
        if not file.is_dir() and not file.name.endswith('.history'):
            start(file.name)


def run(name):
    logging.info(f'Loading user {name}.')
    with open(USER_DIR + name) as f:
        exchange_type, key, secret, enable = f.read().split('\n')

    if enable.lower() == 'disable':
        logging.info('User disabled.')
        return

    if exchange_type != 'Binance':
        logging.error(f'Unknown exchange : {exchange_type}')
        return
    exchange = exchanges.Binance(key, secret)

    logging.info('Client waiting for the next hour ...')
    while True:
        now = datetime.now()

        if now.minute == 0:
            exchange.cancel_orders()
            if exchange.get_balance(exchange.asset_stable) > 6:
                exchange.buy_max_market()

            open_price = exchange.get_open_price()
            limit_price = safe_operators.multiply(open_price, HN)
            time.sleep(2)
            exchange.sell_max_limit(limit_price)
            logging.info(f'TP placed at {open_price}.')
            logging.info('Everything is done for the hour.')

            bitcoin_value = exchange.get_balance(exchange.assets_bitcoin_valuation)
            stable_value = exchange.get_balance(exchange.assets_stable_valuation)
            logging.info(f'Account value : {bitcoin_value} BTC or {stable_value} USD.')

            with open(f'{USER_DIR}{name}.history', 'a+') as f:
                f.write(f'{time.time()}\t{bitcoin_value}\t{stable_value}\n')

            time.sleep(61)

        time.sleep(1)
