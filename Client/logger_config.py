import logging

logging.basicConfig(filename='client_logs.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    level=logging.DEBUG)
