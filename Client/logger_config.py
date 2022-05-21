import logging


def config_client_logger():
    logging.basicConfig(filename='client_logs.log',
                        filemode='a',
                        format='%(levelname)s %(asctime)s - %(message)s',
                        level=logging.DEBUG)
