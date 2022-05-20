import logging

logging.basicConfig(filename=f'server_logs.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    level=logging.DEBUG)
