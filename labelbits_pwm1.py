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

    def annotations(self, data, item):
        if (item.name == "PWM_FIFO"):
            asciilabel = "\""
            asciilabel += chr((data >> 24) & 0xFF)
            asciilabel += chr((data >> 16) & 0xFF)
            asciilabel += chr((data >>  8) & 0xFF)
            asciilabel += chr((data >>  0) & 0xFF)
            asciilabel += "\""
            return asciilabel
        else:
            return str(data)

    def info(self, tag, binary, indent = 32):
        output = ""
        raw = format(binary, "#0" + str(self.bits + 2) + "b")[2:]
        output += (tag + ":\t").expandtabs(indent) + str(raw) + " [LSB]\n\n"
        for item in self.labels:
            data = (binary >> item.shift) & item.mask
            line = str(item.name) + ":\t" + self.cover(binary, item)
            comment = "//" + str(item.comment)
            output += comment + "\n" + line.expandtabs(indent) + " [" + \
                  self.annotations(data, item) + "]\n"
        return output

PWM1_CTL_LABELS = \
[
    label("PWEN1", 0,  0b1, "Channel 1 Enable"),
    label("MODE1", 1,  0b1, "Channel 1 Mode"),
    label("RPTL1", 2,  0b1, "Channel 1 Repeat Last Data"),
    label("SBIT1", 3,  0b1, "Channel 1 Silence Bit"),
    label("POLA1", 4,  0b1, "Channel 1 Polarity"),
    label("USEF1", 5,  0b1, "Channel 1 Use FIFO"),
    label("CLRF",  6,  0b1, "Clear FIFO"),
    label("MSEN1", 7,  0b1, "Channel 1 M/S Enable"),
    label("PWEN2", 8,  0b1, "Channel 2 Enable"),
    label("MODE2", 9,  0b1, "Channel 2 Mode"),
    label("RPTL2", 10, 0b1, "Channel 2 Repeat Last Data"),
    label("SBIT2", 11, 0b1, "Channel 2 Silence Bit"),
    label("POLA2", 12, 0b1, "Channel 2 Polarity"),
    label("USEF2", 13, 0b1, "Channel 2 Use FIFO"),
    label("-",     14, 0b1, "Reserved"),
    label("MSEN2", 15, 0b1, "Channel 2 M/S Enable"),
    label("-",     16, 0b1111111111111111, "Reserved"),
]

PWM1_STA_LABELS = \
[
    label("FULL1", 0,  0b1, "FIFO Full Flag"),
    label("EMPT1", 1,  0b1, "FIFO Empty Flag"),
    label("WERR1", 2,  0b1, "FIFO Write Error Flag"),
    label("RERR1", 3,  0b1, "FIFO Read Error Flag"),
    label("GAPO1", 4,  0b1, "Channel 1 Gap Occurred Flag"),
    label("GAPO2", 5,  0b1, "Channel 2 Gap Occurred Flag"),
    label("-",     6,  0b11, "Reserved"),
    label("BERR",  8,  0b1, "Bus Error Flag"),
    label("STA1",  9,  0b1, "Channel 1 State"),
    label("STA2",  10, 0b1, "Channel 2 State"),
    label("-",     11, 0b111111111111111111111, "Reserved"),
]

PWM1_DMAC_LABELS = \
[
    label("DREQ",     0,  0b11111111, "DMA Threshold for DREQ Signal"),
    label("PANIC",    8,  0b11111111, "DMA Threshold for PANIC Signal"),
    label("-",        16, 0b111111111111111, "Reserved"),
    label("ENAB",     31, 0b1, "DMA Enable"),
]

PWM1_RNG_LABELS = \
[
    label("PWM_RNGi", 0, 0b11111111111111111111111111111111, "Channel i Range"),
]

PWM1_DAT_LABELS = \
[
    label("PWM_DATi", 0, 0b11111111111111111111111111111111, "Channel i Data"),
]

PWM1_FIF1_LABELS = \
[
    label("PWM_FIFO", 0, 0b11111111111111111111111111111111, "Channel FIFO Input"),
]

PWM1_DATA = \
[
    ("PWM1_CTL_LABELS", 0xFE20C800, 0x00000000, PWM1_CTL_LABELS),
    ("PWM1_STA_LABELS", 0xFE20C804, 0x00000002, PWM1_STA_LABELS),
    ("PWM1_DMAC_LABELS", 0xFE20C808, 0x00000707, PWM1_DMAC_LABELS),
    ("PWM1_RNG0_LABELS", 0xFE20C810, 0x00000020, PWM1_RNG_LABELS),
    ("PWM1_DAT0_LABELS", 0xFE20C814, 0x00000000, PWM1_DAT_LABELS),
    ("PWM1_FIF1_LABELS", 0xFE20C818, 0x70776D31, PWM1_FIF1_LABELS),
    ("PWM1_RNG1_LABELS", 0xFE20C820, 0x00000020, PWM1_RNG_LABELS),
    ("PWM1_DAT1_LABELS", 0xFE20C824, 0x00000000, PWM1_DAT_LABELS),
]

output = "<<<LabelBits>>>\n"
spacer = "\n================================================================\n\n"
output += spacer
print(output, end = "")
for data in PWM1_DATA:
    tmp = ""
    PWM1 = labelbits(data[3])
    tmp += PWM1.info(str(data[0]) + " (" + hex(data[1]) + ")", data[2])
    print(tmp, end = "")
    print(spacer, end = "")
    output += tmp + spacer

with open("labelbits_pwm1.txt", "w") as file:
    file.write(output)
