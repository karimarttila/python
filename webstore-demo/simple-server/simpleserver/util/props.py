import os
from configparser import ConfigParser
from pathlib import Path

from simpleserver.util.logger import SSLogger


class Props:
    """Properties class."""

    myLogger = SSLogger(__name__).get_logger()
    SS_PROPERTIES_FILE = 'resources/simpleserver.properties'

    def get_property(self, key) -> str:
        """Gets the value for key"""
        ret = self.parser.get('simpleserver', key)
        return ret

    def __init__(self):
        self.myLogger.debug('cwd: ' + os.getcwd())
        my_file = Path(self.SS_PROPERTIES_FILE)
        if not my_file.is_file():
            buf = "Properties file not found: " + self.SS_PROPERTIES_FILE
            self.myLogger.error(buf)
            raise Exception(buf)
        self.parser = ConfigParser()
        self.parser.read(self.SS_PROPERTIES_FILE)
