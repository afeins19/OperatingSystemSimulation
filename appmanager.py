# this file will hold the user programs that the os will execute
import time
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
        print("[[ TEST_PROCESS_RUNNNG ]]")
        time.sleep(10)


