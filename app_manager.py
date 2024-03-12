# this file will hold the user programs that the os will execute
import time
import logging as lg
from log_config import setup_logger

lgr = setup_logger(__name__)
class AppManager:
    def __init__(self):

        self.name_table = {
            'test' : AppManager.test
        } # maps names to the actual functions for users

    def get_app(self, app_name):
        if app_name in self.name_table.keys():
            return self.name_table[app_name]
        else:
            return None

    # -- processes go here (MUST BE STATIC) --
    @staticmethod
    def test():
        lgr.info("[[ TEST FUNCTION STARTED ]]")
        print("[[ TEST FUNCTION STARTED ]]\n")
        time.sleep(10)
        lgr.info("[[ TEST FUNCTION ENDED ]]")
        print("[[ TEST FUNCTION ENDED ]]\n")



