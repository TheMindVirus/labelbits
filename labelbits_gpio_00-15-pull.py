class label:
    def __init__(self, name = "[LABEL]",
                 shift = 0, mask = 0xFFFFFFFF, comment = "", *args, **kwargs):
        self.name = name
        self.shift = shift
        self.mask = mask
        self.comment = comment;

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

    def mode(self, binary):
        mapping = ["PULL_NONE", "PULL_UP", "PULL_DOWN", "PULL_BOTH"]
        if (binary >= 0) and (binary < len(mapping)):
            return mapping[binary]
        else:
            return str(binary)

    def info(self, binary, indent = 32):
        print("<<<LabelBits>>>")
        raw = format(binary, "#0" + str(self.bits + 2) + "b")[2:]
        print(("Raw Data:\t").expandtabs(indent) + str(raw) + " [LSB]\n")
        for item in self.labels:
            data = (binary >> item.shift) & item.mask
            line = str(item.name) + ":\t" + self.cover(binary, item)
            comment = "//" + str(item.comment)
            print(comment + "\n" + line.expandtabs(indent) + " [" +
                  self.mode(data) + "]\n")

PULL_LABELS = \
[
    label("GPIO_PUP_PDN_CNTRL00", 0,  0b11, "GPIO 00"),
    label("GPIO_PUP_PDN_CNTRL01", 2,  0b11, "GPIO 01"),
    label("GPIO_PUP_PDN_CNTRL02", 4,  0b11, "GPIO 02"),
    label("GPIO_PUP_PDN_CNTRL03", 6,  0b11, "GPIO 03"),
    label("GPIO_PUP_PDN_CNTRL04", 8,  0b11, "GPIO 04"),
    label("GPIO_PUP_PDN_CNTRL05", 10, 0b11, "GPIO 05"),
    label("GPIO_PUP_PDN_CNTRL06", 12, 0b11, "GPIO 06"),
    label("GPIO_PUP_PDN_CNTRL07", 14, 0b11, "GPIO 07"),
    label("GPIO_PUP_PDN_CNTRL08", 16, 0b11, "GPIO 08"),
    label("GPIO_PUP_PDN_CNTRL09", 18, 0b11, "GPIO 09"),
    label("GPIO_PUP_PDN_CNTRL10", 20, 0b11, "GPIO 10"),
    label("GPIO_PUP_PDN_CNTRL11", 22, 0b11, "GPIO 11"),
    label("GPIO_PUP_PDN_CNTRL12", 24, 0b11, "GPIO 12"),
    label("GPIO_PUP_PDN_CNTRL13", 26, 0b11, "GPIO 13"),
    label("GPIO_PUP_PDN_CNTRL14", 28, 0b11, "GPIO 14"),
    label("GPIO_PUP_PDN_CNTRL15", 30, 0b11, "GPIO 15"),
]

GPIO = labelbits(PULL_LABELS)
GPIO.info(0x4AA95555) # Offset 0xE4
