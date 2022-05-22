import logging


def config_server_logger():
    format_ = '%(levelname)s | File "%(filename)s", line %(lineno)s, in %(funcName)s | %(asctime)s - %(message)s'
    logging.basicConfig(filename='server_logs.log',
                        filemode='a',
                        format=format_,
                        level=logging.DEBUG)
