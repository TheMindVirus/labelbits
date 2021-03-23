class label:
    def __init__(self, name = "[LABEL]",
                 shift = 0, mask = 0xFFFFFFFF, *args, **kwargs):
        self.name = name
        self.shift = shift
        self.mask = mask

class labelbits:
    def __init__(self, labels = [], bits = 32, *args, **kwargs):
        self.bits = bits
        self.labels = labels

    def cover(self, binary, item):
        masked = ""
        mask = item.mask << item.shift
        for i in range(self.bits -1, -1, -1):
            if ((mask >> i) & 1):
                masked += str((binary >> i) & 1)
            else:
                masked += "-"
        return masked

    def info(self, binary, indent = 32):
        print("<<<LabelBits>>>")
        raw = format(binary, "#0" + str(self.bits + 2) + "b")[2:]
        print(("Raw Data:\t").expandtabs(indent) + str(raw) + " [LSB]\n")
        for item in self.labels:
            data = (binary >> item.shift) & item.mask
            line = str(item.name) + ":\t" + self.cover(binary, item)
            print(line.expandtabs(indent) + " [" + str(data) + "]\n")

BIT     = 1
CRUMB   = 2
NIBBLE  = 4
BYTE    = 8
WORD    = 16
DWORD   = 32
QWORD   = 64
PARA    = 128
DPARA   = 256
QPARA   = 512
HPAGE   = 1024
SPAGE   = 2048
DPAGE   = 4096
QPAGE   = 8192

TRIAD    = 3
HEPTAD   = 7
DECLET   = 10
DODECLET = 12
TWORD    = 48
BENTOBOX = 96
CENTLET  = 100
AES      = 192
MTU      = 1500

DEVICE_POWER_STATE = DWORD
SYSTEM_POWER_STATE = DWORD
POWER_SYSTEM_MAXIMUM = 7

def increment(var, count):
    tmp = var[0]
    var[0] += count
    return (tmp, pow(2, count) - 1)

def genlabels():
    i = [0]
    labels = []
    labels.append(label("Size",                    *increment(i, WORD)))
    labels.append(label("Version",                 *increment(i, WORD)))
    labels.append(label("DeviceD1",                *increment(i, BIT)))
    labels.append(label("DeviceD2",                *increment(i, BIT)))
    labels.append(label("LockSupported",           *increment(i, BIT)))
    labels.append(label("EjectSupported",          *increment(i, BIT)))
    labels.append(label("Removable",               *increment(i, BIT)))
    labels.append(label("DockDevice",              *increment(i, BIT)))
    labels.append(label("UniqueID",                *increment(i, BIT)))
    labels.append(label("SilentInstall",           *increment(i, BIT)))
    labels.append(label("RawDeviceOK",             *increment(i, BIT)))
    labels.append(label("SurpriseRemovalOK",       *increment(i, BIT)))
    labels.append(label("WakeFromD0",              *increment(i, BIT)))
    labels.append(label("WakeFromD1",              *increment(i, BIT)))
    labels.append(label("WakeFromD2",              *increment(i, BIT)))
    labels.append(label("WakeFromD3",              *increment(i, BIT)))
    labels.append(label("HardwareDisabled",        *increment(i, BIT)))
    labels.append(label("NonDynamic",              *increment(i, BIT)))
    labels.append(label("WarmEjectSupported",      *increment(i, BIT)))
    labels.append(label("NoDisplayInUI",           *increment(i, BIT)))
    labels.append(label("Reserved1",               *increment(i, BIT)))
    labels.append(label("WakeFromInterrupt",       *increment(i, BIT)))
    labels.append(label("SecureDevice",            *increment(i, BIT)))
    labels.append(label("ChildOfVgaEnabledBridge", *increment(i, BIT)))
    labels.append(label("DecodeIoOnBoot",          *increment(i, BIT)))
    labels.append(label("Reserved",                *increment(i, 0b111111111)))
    labels.append(label("Address",                 *increment(i, DWORD)))
    labels.append(label("UINumber",                *increment(i, DWORD)))
    labels.append(label("DeviceState",             *increment(i, DEVICE_POWER_STATE * POWER_SYSTEM_MAXIMUM)))
    labels.append(label("SystemWake",              *increment(i, SYSTEM_POWER_STATE)))
    labels.append(label("DeviceWake",              *increment(i, DEVICE_POWER_STATE)))
    labels.append(label("D1Latency",               *increment(i, DWORD)))
    labels.append(label("D2Latency",               *increment(i, DWORD)))
    labels.append(label("D3Latency",               *increment(i, DWORD)))
    return (labels, i[0])

Capabilities = labelbits(*genlabels())
Capabilities.info(0x00000084)
#Capabilities.info(0x00000080)
#Capabilities.info(0x00000004)
#Capabilities.info(0x00000090)
#Capabilities.info(0x00000094)
#Capabilities.info(0x00000014)
#Capabilities.info(0x000000a0)
#Capabilities.info(0x00000000) #USBSTOR
#Capabilities.info(0x00000010) #USBSTOR
#More at: Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB\<device>\<ID>\Capabilities
#And also: Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR\<device>\<ID>\Capabilities
#https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_device_capabilities
