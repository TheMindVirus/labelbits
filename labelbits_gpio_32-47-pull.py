class label:
    def __init__(self, name = "[LABEL]",
                 shift = 0, mask = 0xFFFFFFFF, comment = "", annotation = "", *args, **kwargs):
        self.name = name
        self.shift = shift
        self.mask = mask
        self.comment = comment
        self.annotation = annotation

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
                  self.mode(data) + "]\t" + item.annotation + "\n")

PULL_LABELS = \
[
    label("GPIO_PUP_PDN_CNTRL32", 0,  0b11, "GPIO 32"),
    label("GPIO_PUP_PDN_CNTRL33", 2,  0b11, "GPIO 33"),
    label("GPIO_PUP_PDN_CNTRL34", 4,  0b11, "GPIO 34"),
    label("GPIO_PUP_PDN_CNTRL35", 6,  0b11, "GPIO 35"),
    label("GPIO_PUP_PDN_CNTRL36", 8,  0b11, "GPIO 36"),
    label("GPIO_PUP_PDN_CNTRL37", 10, 0b11, "GPIO 37"),
    label("GPIO_PUP_PDN_CNTRL38", 12, 0b11, "GPIO 38"),
    label("GPIO_PUP_PDN_CNTRL39", 14, 0b11, "GPIO 39"),
    label("GPIO_PUP_PDN_CNTRL40", 16, 0b11, "GPIO 40", "//Headphone R"),
    label("GPIO_PUP_PDN_CNTRL41", 18, 0b11, "GPIO 41", "//Headphone L"),
    label("GPIO_PUP_PDN_CNTRL42", 20, 0b11, "GPIO 42"),
    label("GPIO_PUP_PDN_CNTRL43", 22, 0b11, "GPIO 43"),
    label("GPIO_PUP_PDN_CNTRL44", 24, 0b11, "GPIO 44"),
    label("GPIO_PUP_PDN_CNTRL45", 26, 0b11, "GPIO 45"),
    label("GPIO_PUP_PDN_CNTRL46", 28, 0b11, "GPIO 46"),
    label("GPIO_PUP_PDN_CNTRL47", 30, 0b11, "GPIO 47"),
]

GPIO = labelbits(PULL_LABELS)
GPIO.info(0xA550555A) # Offset 0xEC
