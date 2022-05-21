import logging


def config_server_logger():
    logging.basicConfig(filename='server_logs.log',
                        filemode='a',
                        format='%(levelname)s %(asctime)s - %(message)s',
                        level=logging.DEBUG)
