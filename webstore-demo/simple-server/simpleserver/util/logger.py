import logging
import logging.config

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

class SSLogger:

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)

    def get_logger(self):
        return self.logger


