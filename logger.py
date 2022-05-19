import logging
from datetime import datetime


class Logger:
    def __init__(self):
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        today_date = datetime.today().strftime('%Y-%m-%d')
        logging.basicConfig(filename=f'{today_date}.log',
                            filemode="w",
                            format=Log_Format,
                            level=logging.ERROR)

        self.logger = logging.getLogger()

        # Testing our Logger

        self.logger.error("Our First Log Message")

    def write_debug_log(self, log_msg):
        self.logger.debug(log_msg)

    def write_info_log(self, log_msg):
        logging.info(log_msg)

    def write_warning_log(self, log_msg):
        logging.warning(log_msg)

    def write_error_log(self, log_msg):
        logging.error(log_msg)

    def write_critical_log(self, log_msg):
        logging.critical(log_msg)

    def write_excetion_log(self, log_msg):
        logging.exception(log_msg)
