import platform
import psutil
from datetime import datetime

class systemInformation:

    def __init__(self):
        self._generalInformation = ''
        self.gatherGeneralInfo()

    # [IN WORKING] Funzione utilizzata per il retrieval delle informazioni di base
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        self._generalInformation = self._generalInformation + deviceName.processor + '#'

