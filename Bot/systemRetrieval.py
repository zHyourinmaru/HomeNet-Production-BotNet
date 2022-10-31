import platform
import psutil
from datetime import datetime

class systemInformation:

    def __init__(self):
        self._generalInformation = ''
        self._bootInformation = ''
        #self.gatherGeneralInfo()
        self.gatherBootInfo()

    # [IN WORKING] Funzione utilizzata per il retrieval delle informazioni di base
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        self._generalInformation = self._generalInformation + deviceName.processor + '#'

    # Funzione per il retrieval delle informazioni su data e ora
    def gatherBootInfo(self):
        boot_time_timestamp = psutil.boot_time()
        boot = datetime.fromtimestamp(boot_time_timestamp)
        self._bootInformation = str(boot.day) + '/' + str(boot.month) + '/' + str(boot.year) + ' '
        self._bootInformation = self._bootInformation + str(boot.hour) + ':' + str(boot.minute) + ':' + str(boot.second)


