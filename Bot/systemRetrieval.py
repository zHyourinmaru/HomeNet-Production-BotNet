
import platform
import psutil
from datetime import datetime

# [FUNCTION DESCRIPTION] Converte la quantità di bytes nel formato migliore (KB, MB, GB, etc.).
def get_size(b):
    if b < 1000:
        return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b / 1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b / 1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b / 1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b / 1000000000000) + 'TB'

class SystemInformation:
    def __init__(self):
        self._generalInformation = ''
        self._cpuInformation = ''
        self._memoryInformation = ''
        self.systemRetrieval()

    def systemRetrieval(self):
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self.gatherMemoryInfo()
        self.gatherDiskUsage()
        self._generalInformation = self._generalInformation + self._cpuInformation + self._memoryInformation

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni di base del sistema.
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        bootTimeInfo = psutil.boot_time()
        bTime = datetime.fromtimestamp(bootTimeInfo)
        self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        self._generalInformation = self._generalInformation + deviceName.processor
        self._generalInformation = self._generalInformation + str(bTime.day) + '/' + str(bTime.month) + '/' + str(bTime.year) + '#'
        self._generalInformation = self._generalInformation + 'Boot time: ' + str(bTime.hour) + ':' + str(bTime.minute) + ':' + str(bTime.second) + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative alla CPU.
    def gatherCpuInfo(self):
        self._cpuInformation = str(psutil.cpu_count(logical=False)) + '#' + str(psutil.cpu_count(logical=True)) + '#'
        cpufrequencies = psutil.cpu_freq()
        self._cpuInformation = self._cpuInformation + str(cpufrequencies.max) + '#' + str(cpufrequencies.min) + '#' + str(cpufrequencies.current)
        self._cpuInformation = self._cpuInformation + '#' + str(psutil.cpu_percent()) + '#'

        usage_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            usage_core = usage_core + '' + str(i+1) + ') ' + str(percentage) + '%' + ' -- '

        self._cpuInformation = self._cpuInformation + usage_core + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative all'utilizzo della memoria.
    def gatherMemoryInfo(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        """
            psutil.virtual_memory() ritorna le stats relative alle informazioni sull'utilizzo della memoria come una namedtuple.
            La namedtuple conserva campi come 'total physical memory available', 'available memory (i.e not used)', 'used', 'percentage'.
            psutil.swap_memory() è la stessa cosa ma per swap memory.
        """
        self._memoryInformation = self._memoryInformation + '\n'
        self._memoryInformation = self._memoryInformation + 'Total: ' + str(get_size(mem.total)) + '#Available: ' + str(get_size(mem.available)) + '#Used: ' + str(get_size(mem.used)) + '#Percentage: '
        self._memoryInformation = self._memoryInformation + str(get_size(mem.percent)) + '%'
        self._memoryInformation = self._memoryInformation + '#Swap memory total: ' + str(get_size(swap.total)) + '#Swap memory free: ' + str(get_size(swap.free)) + '#Swap memory used: ' + str(get_size(swap.used)) + '#Swap memory percentage: '
        self._memoryInformation = self._memoryInformation + str(get_size(swap.percent)) + '%#'

    #[EDA VEDERE E FARE PER BEN]
    def gatherDiskUsage(self):
        # Disk Information
        print("=" * 40, "Disk Information", "=" * 40)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")


    # Manca: Network Information.