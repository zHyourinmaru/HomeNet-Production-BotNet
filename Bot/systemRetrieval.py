import platform
import psutil

from datetime import datetime

# [FUNCTION DESCRIPTION] Converte la quantità di bytes nel formato migliore (KB, MB, GB, etc.).
def get_size(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

class SystemInformation:
    def __init__(self):
        self.data = {}

        self._generalInformation = {}
        self._generalInformation = {}
        self._cpuInformation = {}
        self._memoryInformation = {}
        self._diskInformation = {}

        self.systemRetrieval()

    def systemRetrieval(self):
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self.gatherMemoryInfo()
        self.gatherDiskUsage()

        self.data['GeneralInformation'] = self._generalInformation
        self.data['CPUInformation'] = self._cpuInformation
        self.data['MemoryInformation'] = self._memoryInformation
        self.data['DiskInformation'] = self._diskInformation


    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni di base del sistema.
    def gatherGeneralInfo(self):
        deviceName = platform.uname()
        bootTimeInfo = psutil.boot_time()
        bTime = datetime.fromtimestamp(bootTimeInfo)

        self._generalInformation['System'] = deviceName.system
        self._generalInformation['Node'] = deviceName.node
        self._generalInformation['Release'] = deviceName.release
        self._generalInformation['Version'] = deviceName.version
        self._generalInformation['Machine'] = deviceName.machine
        self._generalInformation['Processor'] = deviceName.processor
        self._generalInformation['Date'] = str(bTime.day) + '/' + str(bTime.month) + '/' + str(bTime.year)
        self._generalInformation['BootTime'] = str(bTime.hour) + ':' + str(bTime.minute) + ':' + str(bTime.second)

        #self._generalInformation = deviceName.system + '#' + deviceName.node + '#' + deviceName.release + '#'
        #self._generalInformation = self._generalInformation + deviceName.version + '#' + deviceName.machine + '#'
        #self._generalInformation = self._generalInformation + deviceName.processor
        #self._generalInformation = self._generalInformation + str(bTime.day) + '/' + str(bTime.month) + '/' + str(bTime.year) + '#'
        #self._generalInformation = self._generalInformation + 'Boot time: ' + str(bTime.hour) + ':' + str(bTime.minute) + ':' + str(bTime.second) + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative alla CPU.
    def gatherCpuInfo(self):
        self._cpuInformation['LogicalFalse'] = str(psutil.cpu_count(logical=False)) # core
        self._cpuInformation['LogicalTrue'] = str(psutil.cpu_count(logical=True)) # nel caso thread chiediamo a simone

        #self._cpuInformation = str(psutil.cpu_count(logical=False)) + '#' + str(psutil.cpu_count(logical=True)) + '#'
        cpufrequencies = psutil.cpu_freq()

        self._cpuInformation['Max'] = str(cpufrequencies.max)
        self._cpuInformation['Min'] = str(cpufrequencies.min)
        self._cpuInformation['Current'] = str(cpufrequencies.max)

        self._cpuInformation['Percentage'] = str(psutil.cpu_percent())

        #self._cpuInformation = self._cpuInformation + str(cpufrequencies.max) + '#' + str(cpufrequencies.min) + '#' + str(cpufrequencies.current)
        #self._cpuInformation = self._cpuInformation + '#' + str(psutil.cpu_percent()) + '#'

        usage_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            usage_core = usage_core + '' + str(i+1) + ') ' + str(percentage) + '%' + ' -- '

        self._cpuInformation['Cores'] = str(usage_core)
        #self._cpuInformation = self._cpuInformation + usage_core + '#'

    # [FUNCTION DESCRIPTION] Procedura utilizzata per il retrieval delle informazioni relative all'utilizzo della memoria.
    def gatherMemoryInfo(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        """
            psutil.virtual_memory() ritorna le stats relative alle informazioni sull'utilizzo della memoria come una namedtuple.
            La namedtuple conserva campi come 'total physical memory available', 'available memory (i.e not used)', 'used', 'percentage'.
            psutil.swap_memory() è la stessa cosa ma per swap memory.
        """

        self._memoryInformation['Total'] = str(get_size(mem.total))
        self._memoryInformation['Available'] = str(get_size(mem.available))
        self._memoryInformation['Used'] = str(get_size(mem.used))
        self._memoryInformation['Percentage'] = str(get_size(mem.percent))
        self._memoryInformation['SwapTotal'] = str(get_size(swap.total))
        self._memoryInformation['SwapFree'] = str(get_size(swap.free))
        self._memoryInformation['SwapTotal'] = str(get_size(swap.total))
        self._memoryInformation['SwapUsed'] = str(get_size(swap.used))
        self._memoryInformation['SwapPercentage'] = str(get_size(swap.percent))


        #self._memoryInformation = self._memoryInformation + '\n'
        #self._memoryInformation = self._memoryInformation + 'Total: ' + str(get_size(mem.total)) + '#Available: ' + str(get_size(mem.available)) + '#Used: ' + str(get_size(mem.used)) + '#Percentage: '
        #self._memoryInformation = self._memoryInformation + str(get_size(mem.percent)) + '%'
        #self._memoryInformation = self._memoryInformation + '#Swap memory total: ' + str(get_size(swap.total)) + '#Swap memory free: ' + str(get_size(swap.free)) + '#Swap memory used: ' + str(get_size(swap.used)) + '#Swap memory percentage: '
        #self._memoryInformation = self._memoryInformation + str(get_size(swap.percent)) + '%#'

    #[DA VEDERE E FARE PER BENE]
    def gatherDiskUsage(self):
        # Disk Information

        # get all disk partitions
        partition_Informations = psutil.disk_partitions()
        partitions = []

        for i,partition in enumerate(partition_Informations):
            partitions.append({
                'Device': partition.device,
                'Mountpoint': partition.mountpoint,
                'FStype': partition.fstype
            })

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                print("Permission error")
                continue

            partitions[i]['TotalSize'] = get_size(partition_usage.total)
            partitions[i]['Used'] = get_size(partition_usage.used)
            partitions[i]['Free'] = get_size(partition_usage.free)
            partitions[i]['Percentage'] = partition_usage.percent

        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()

        self._diskInformation['Partitions'] = partitions
        self._diskInformation['TotalRead'] = get_size(disk_io.read_bytes)
        self._diskInformation['TotalWrite'] = get_size(disk_io.read_bytes)


    # Manca: Network Information.