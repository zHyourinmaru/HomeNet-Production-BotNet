import platform
import psutil
import GPUtil
import os
import ctypes

from datetime import datetime

# Classe sottostante completamente copiata, serve per far leggere alcune directory che hanno un problema, per via di
# windows che fa funziona un "redirector", non so che spaccetta sia, capiamo.
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def get_size(B):
    """
    Procedura per la rappresentazione della quantità espressa in bytes nel formato migliore (KB, MB, GB, etc.).
    :param B: rappresenta la quantità in byte da rappresentare nel giusto formato.
    :return: string
    """
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
        self.data = {} # Rappresenta la collezione di dati nella sua interezza. E' composta da tante piccole "sotto-collezioni".

        # Sotto-collezioni che compongono data:
        self._generalInformation = {}
        self._generalInformation = {}
        self._cpuInformation = {}
        self._memoryInformation = {}
        self._diskInformation = {}
        self._networkInformation = {}
        self._gpuInformation = {}
        self._fileInformation = {}

        self.systemRetrieval()

    def systemRetrieval(self):
        """
        In tale procedura si raccolgono i dati che poi comporranno il file .json
        :return: None
        """
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self.gatherMemoryInfo()
        self.gatherDiskUsage()
        self.gatherNetworkInfo()
        self.gatherGpuInfo()
        self.gatherFileInformation()

        self.data['GeneralInformation'] = self._generalInformation
        self.data['CPUInformation'] = self._cpuInformation
        self.data['MemoryInformation'] = self._memoryInformation
        self.data['DiskInformation'] = self._diskInformation
        self.data['NetworkInformation'] = self._networkInformation
        self.data['GpuInformation'] = self._gpuInformation
        self.data['FileInformation'] = self._fileInformation


    def gatherGeneralInfo(self):
        """
        Procedura nella quale si effettua retrieval delle informazioni di base (generali) del sistema.
        Si compone la sotto-collezione '_generalInformation' da poi inserire in 'data'.
        :return: None
        """
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


    def gatherCpuInfo(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative alla CPU.
        Si compone la sotto-collezione '_cpuInformation' da poi inserire in 'data'.
        :return: None
        """
        self._cpuInformation['PhysicalCores'] = str(psutil.cpu_count(logical=False))
        self._cpuInformation['TotalCores'] = str(psutil.cpu_count(logical=True))

        cpufrequencies = psutil.cpu_freq()

        self._cpuInformation['Max'] = str(cpufrequencies.max)
        self._cpuInformation['Min'] = str(cpufrequencies.min)
        self._cpuInformation['Current'] = str(cpufrequencies.max)
        self._cpuInformation['Percentage'] = str(psutil.cpu_percent())

        usage_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            usage_core = usage_core + '' + str(i+1) + ') ' + str(percentage) + '%' + ' -- '

        self._cpuInformation['Cores'] = str(usage_core)


    def gatherMemoryInfo(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative all'utilizzo della memoria.
        Si compone la sotto-collezione '_memoryInformation' da poi inserire in 'data'.
        :return: None
        """
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


    def gatherDiskUsage(self): # [FUNZIONANTE MA DA RIGUARDARE]
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative all'utilizzo del disco.
        Si compone la sotto-collezione '_diskInformation' da poi inserire in 'data'.
        :return: None
        """

        # otteniamo tutte le partizioni.
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
                # potrebbe generarsi un'eccezione nel caso in cui il disco non sia pronto.
                print("Permission error")
                continue

            partitions[i]['TotalSize'] = get_size(partition_usage.total)
            partitions[i]['Used'] = get_size(partition_usage.used)
            partitions[i]['Free'] = get_size(partition_usage.free)
            partitions[i]['Percentage'] = partition_usage.percent

        # IO statistics a partire dal boot.
        disk_io = psutil.disk_io_counters()

        self._diskInformation['Partitions'] = partitions
        self._diskInformation['TotalRead'] = get_size(disk_io.read_bytes)
        self._diskInformation['TotalWrite'] = get_size(disk_io.read_bytes)


    def gatherNetworkInfo(self): # [FUNZIONANTE MA DA RIGUARDARE E SISTEMARE IL COMMENTO DELLA PROCEDURA]
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative alla rete.
        Si compone la sotto-collezione '_networkInformation' da poi inserire in 'data'.
        :return: None
        """

        # otteniamo le interfacce di rete (virtuali e fisiche)
        if_addrs = psutil.net_if_addrs()
        indirizzi = []

        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:

                if str(address.family) == 'AddressFamily.AF_INET':
                    indirizzi.append({
                        'IP Address': address.address,
                        'Netmask': address.netmask,
                        'Broadcast IP': address.broadcast
                    })
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    indirizzi.append({
                        'MAC Address': address.address,
                        'Netmask': address.netmask,
                        'Broadcast MAC': address.broadcast
                    })
                #print(f"=== Interface: {interface_name} ===")
                #if str(address.family) == 'AddressFamily.AF_INET':
                #    print(f"  IP Address: {address.address}")
                #    print(f"  Netmask: {address.netmask}")
                #    print(f"  Broadcast IP: {address.broadcast}")
                #elif str(address.family) == 'AddressFamily.AF_PACKET':
                #    print(f"  MAC Address: {address.address}")
                #    print(f"  Netmask: {address.netmask}")
                #    print(f"  Broadcast MAC: {address.broadcast}")
        # IO statistics a partire dal boot.
        net_io = psutil.net_io_counters()
        self._networkInformation['Active Address'] = indirizzi
        self._networkInformation['Total Bytes Sent'] = get_size((net_io.bytes_sent))
        self._networkInformation['Total Bytes Received'] = get_size((net_io.bytes_recv))

    def gatherGpuInfo(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative alla scheda grafica.
        Si compone la sotto-collezione '_gpuInformation' da poi inserire in 'data'.
        :return: None
        """

        deviceGpu = GPUtil.getGPUs()
        listGpu = []

        for i,gpu in enumerate(deviceGpu):
            listGpu.append({
                'Id': gpu.id,
                'Name': gpu.name,
                'Load': f"{gpu.load*100}%",
                'Free Memory': f"{gpu.memoryFree}MB",
                'Used Memory': f"{gpu.memoryUsed}MB",
                'Total Memory': f"{gpu.memoryTotal}MB",
                'Temperature': f"{gpu.temperature} °C",
                'UUID': gpu.uuid
            })

        self._gpuInformation['Gpu'] = listGpu

    def gatherFileInformation(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative ai file.
        Si compone la sotto-collezione '_fileInformation' da poi inserire in 'data'.
        :return: None
        """
        path = "\\"
        dir_list = os.listdir(path)
        self._fileInformation ['File'] = dir_list
        for element in dir_list:
            try:
                path = "/" + element
                if os.path.isdir(path):
                    print("nel file "+ element + " è presente: ")
                    with disable_file_system_redirection():
                        print(os.listdir(path))
                elif os.path.isfile(path):
                    print(element + " e' un file.")
                else:
                    print(element + " e' un file speciale, come una Socket o Device File.")
            except IOError:
                print("Impossibile aprire il file " + element)

    #Funzione per trovare tutti i file di testo -- da vedere come aprirli tramite questa procedura + da aggiungere a data
    def allTxtInformation(self):
        """
        Procedura nella quale si effettua il retrieval dei file di testo (.txt).
        :return: None
        """
        for root, dirs, files in os.walk("/"):
            for name in files:
                if name.endswith(".txt"):
                    print(name)

            for name in dirs:
                if name.endswith(".txt"):
                    print(name)







