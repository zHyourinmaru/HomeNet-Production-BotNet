import platform
import psutil
from datetime import datetime

class systemInformation:
    def __init__(self):
        self._generalInformation = ''
        self._cpuInformation = ''
        self._memoryInformation = ''
        self.systemRetrieval()

    def systemRetrieval(self):
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self.gatherMemoryInfo()
        #
        self._generalInformation = self._generalInformation + self._cpuInformation + self._memoryInformation # +

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni di base del sistema.
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        bootTimeInfo = psutil.boot_time()
        bTime = datetime.fromtimestamp(bootTimeInfo)
        self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        self._generalInformation = self._generalInformation + deviceName.processor + '#Current date: '
        self._generalInformation = self._generalInformation + str(bTime.day) + '/' + str(bTime.month) + '/' + str(bTime.year) + '#'
        self._generalInformation = self._generalInformation + 'Boot time: ' + str(bTime.hour) + ':' + str(bTime.minute) + ':' + str(bTime.second) + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative alla CPU.
    def gatherCpuInfo(self):
        self._cpuInformation = '\nNumber of physical cores: ' + str(psutil.cpu_count(logical=False)) + '#Total cores: ' + str(psutil.cpu_count(logical=True)) + '#'
        cpufrequencies = psutil.cpu_freq()
        self._cpuInformation = self._cpuInformation + 'Max frequency: ' + str(cpufrequencies.max) + ' Mhz #Min frequency: ' + str(cpufrequencies.min) + ' Mhz #Current frequency: ' + str(cpufrequencies.current) + ' Mhz'
        self._cpuInformation = self._cpuInformation + '#Total Cpu usage: ' + str(psutil.cpu_percent()) + '%#Cpu usage per core: '

        usage_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            usage_core = usage_core + '' + str(i+1) + ') ' + str(percentage) + '%' + ' -- '

        self._cpuInformation = self._cpuInformation + usage_core + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative all'utilizzo della memoria.
    """
        TODO: mem.total -> la quantità è in byte e va scalata in kilobyte, megabyte, etc. 
    """
    def gatherMemoryInfo(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        """
            psutil.virtual_memory() ritorna le stats relative alle informazioni sull'utilizzo della memoria come una namedtuple.
            La namedtuple conserva campi come 'total physical memory available', 'available memory (i.e not used)', 'used', 'percentage'.
            
            psutil.swap_memory() è la stessa cosa ma per swap memory.
        """
        self._memoryInformation = self._memoryInformation + '\n'
        self._memoryInformation = self._memoryInformation + 'Total: ' + str(mem.total) + '#Available: ' + str(mem.available) + '#Used: ' + str(mem.used) + '#Percentage: '
        self._memoryInformation = self._memoryInformation + str(mem.percent) + '%'
        self._memoryInformation = self._memoryInformation + '#Swap memory total: ' + str(swap.total) + '#Swap memory free: ' + str(swap.free) + '#Swap memory used: ' + str(swap.used) + '#Swap memory percentage: '
        self._memoryInformation = self._memoryInformation + str(swap.percent) + '%#'

    """
        Mancano: Disk Usage, Network Information.
    """