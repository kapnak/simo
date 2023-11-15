import logging
from logging.handlers import TimedRotatingFileHandler

import user

file_handler = TimedRotatingFileHandler('logs/simo', when='midnight')
file_handler.suffix += '.log'

stream_handler = logging.StreamHandler()

logging.basicConfig(
    format='%(asctime)s\t[%(levelname)s]\t(%(module)s.%(funcName)s)\t%(threadName)s\t%(message)s',
    level=logging.DEBUG,
    handlers=[file_handler, stream_handler]
)

user.start_all()
