import platform
import psutil
from datetime import datetime

class systemInformation:

    def __init__(self):
        self._generalInformation = ''
        self._cpuinformation = ''
        self.systemRetrieval()

    def systemRetrieval(self):
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self._generalInformation = self._generalInformation + self._cpuinformation

    # [IN WORKING] Funzione utilizzata per il retrieval delle informazioni di base
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        self._generalInformation = self._generalInformation + deviceName.processor + '#'

    def gatherCpuInfo(self):
        self._cpuinformation = '\nNumber of physical cores: ' + str(psutil.cpu_count(logical=False)) + '# Total cores: ' + str(psutil.cpu_count(logical=True)) + '# '
        cpufrequencies = psutil.cpu_freq()
        self._cpuinformation = self._cpuinformation + 'Max frequency: ' + str(cpufrequencies.max) + ' Mhz # Min frequency: ' + str(cpufrequencies.min) + ' Mhz # Current frequency: ' + str(cpufrequencies.current) + ' Mhz # '
        # manca la percentuale di utilizzo della cpu