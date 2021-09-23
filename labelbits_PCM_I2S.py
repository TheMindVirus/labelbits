import copy

class label:
    def __init__(self, *args):
        self.name = "[LABEL]"
        self.start = 0
        self.end = 0
        self.comment = ""
        self.mode = ""
        
        l = len(args)
        if (l > 0):
            self.name = args[0]
            self.start = args[1]
            self.end = self.start
            if (l < 5):
                self.comment = args[2]
                self.mode = args[3]
            else:
                self.end = args[2]
                self.comment = args[3]
                self.mode = args[4]

        if (self.start > self.end):
            self.start, self.end = [self.end, self.start]

class labelbits:
    def __init__(self, labels = [], bits = 32, *args, **kwargs):
        self.bits = bits
        self.labels = labels

    #def mask(a, b):
    #    return bin(((1 << (b - a) + 1) - 1) << a)

    def cover(self, binary, item):
        masked = ""
        mask = (1 << (item.end - item.start) + 1) - 1
        mask <<= item.start
        for i in range(self.bits -1, -1, -1):
            if ((mask >> i) & 1):
                masked += str((binary >> i) & 1)
            else:
                masked += "-"
        return masked

    def info(self, header, binary, indent = 32, dashes = 64, dashtype = "_"):
        print((dashtype * 3) + "[" + header + "]" + (dashtype * (dashes - len(header) - 5)) + "\n")
        raw = format(binary, "#0" + str(self.bits + 2) + "b")[2:]
        print(("Raw Data:\t").expandtabs(indent) + str(raw) + " [LSB]\n")
        for item in self.labels:
            mask = (1 << (item.end - item.start) + 1) - 1
            mask <<= item.start
            data = (binary >> item.start) & mask
            line = str(item.name) + ":\t" + self.cover(binary, item)
            comment = "//" + str(item.comment)
            print(comment + "\n" + line.expandtabs(indent) + " [" + item.mode + "]\n")
        print((dashtype * dashes) + "\n")

PCM_I2S_CS_A_LABELS = \
[
    label("EN", 0, "Enable the PCM Audio Interface", "RW"),
    label("RXON", 1, "Enable Reception", "RW"),
    label("TXON", 2, "Enable Transmission", "RW"),
    label("TXCLR", 3, "Clear the TX FIFO", "W1SC"),
    label("RXCLR", 4, "Clear the RX FIFO", "W1SC"),
    label("TXTHR", 5, 6, "TXW Flag Trigger Threshold", "RW"),
    label("RXTHR", 7, 8, "RXR Flag Trigger Threshold", "RW"),
    label("DMAEN", 9, "DMA DREQ Enable", "RW"),
    label("-", 10, 12, "Reserved", "-"),
    label("TXSYNC", 13, "TX FIFO Synchronisation", "RO"),
    label("RXSYNC", 14, "RX FIFO Synchronisation", "RO"),
    label("TXERR", 15, "TX FIFO Error", "W1C"),
    label("RXERR", 16, "RX FIFO Error", "W1C"),
    label("TXW", 17, "TX FIFO needs Writing", "RO"),
    label("RXR", 18, "RXR FIFO needs Reading", "RO"),
    label("TXD", 19, "TX FIFO can Accept Data", "RO"),
    label("RXD", 20, "RX FIFO contains Data", "RO"),
    label("TXE", 21, "TX FIFO is Empty", "RO"),
    label("RXF", 22, "RX FIFO is Full", "RO"),
    label("RXSEX", 23, "RX Sign Extend", "RW"),
    label("SYNC", 24, "PCM Clock Synchronisation Helper", "RW"),
    label("-", 25, 31, "Reserved", "-")
]

PCM_I2S_FIFO_A_LABELS = \
[
    label("FIFO", 0, 31, "Write to Transmit, Read to Receive", "RW")
]

PCM_I2S_MODE_A_LABELS = \
[
    label("FSLEN", 0, 9, "Frame Synchronisation Length", "RW"),
    label("FLEN", 10, 19, "Frame Length", "RW"),
    label("FSI", 20, "Frame Synchronisation Invert", "RW"),
    label("FSM", 21, "Frame Synchronisation Mode", "RW"),
    label("CLKI", 22, "Clock Invert", "RW"),
    label("CLKM", 23, "PCM Clock Mode", "RW"),
    label("FTXP", 24, "Transmit Frame Packed Mode", "RW"),
    label("FRXP", 25, "Receive Frame Packed Mode", "RW"),
    label("PDME", 26, "PDM Input Mode Enable", "RW"),
    label("PDMN", 27, "PDM Decimation Factor", "RW"),
    label("CLK_DIS", 28, "PCM Clock Disable", "RW"),
    label("-", 29, 31, "Reserved", "-"),
]

PCM_I2S_TXC_A_RXC_A_LABELS = \
[
    label("CH1EN", 30, "Channel 1 Enable", "RW"),
    label("CH1POS", 29, 20, "Channel 1 Position", "RW"),
    label("CH1WID", 19, 16, "Channel 1 Width", "RW"),
    label("CH1WEX", 31, "Channel 1 Width Extension Bit", "RW"),
    label("CH2EN", 14, "Channel 2 Enable", "RW"),
    label("CH2POS", 13, 4, "Channel 2 Position", "RW"),
    label("CH2WID", 3, 0, "Channel 2 Width", "RW"),
    label("CH2WEX", 15, "Channel 2 Width Extension Bit", "RW"),
]

PCM_I2S_DREQ_A_LABELS = \
[
    label("RX_REQ", 0, 6, "RX Request Level", "RW"),
    label("-", 7, "Reserved", "-"),
    label("TX_REQ", 8, 14, "TX Request Level", "RW"),
    label("-", 15, "Reserved", "-"),
    label("RX_PANIC", 16, 22, "RX Panic Level", "RW"),
    label("-", 23, "Reserved", "-"),
    label("TX_PANIC", 24, 30, "TX Panic Level", "RW"),
    label("-", 31, "Reserved", "-"),
]

PCM_I2S_INTEN_A_LABELS = \
[
    label("TXW", 0, "TX Write Interrupt Enable", "RW"),
    label("RXR", 1, "RX Read Interrupt Enable", "RW"),
    label("TXERR", 2, "TX Error Interrupt", "RW"),
    label("RXERR", 3, "RX Error Interrupt", "RW"),
    label("-", 4, 31, "Reserved", "-"),
]

PCM_I2S_INTSTC_A_LABELS = copy.deepcopy(PCM_I2S_INTEN_A_LABELS)
PCM_I2S_INTSTC_A_LABELS[0].comment = "TX Write Interrupt Status / Clear"
PCM_I2S_INTSTC_A_LABELS[1].comment = "RX Read Interrupt Status / Clear"
PCM_I2S_INTSTC_A_LABELS[2].comment = "TX Error Interrupt Status / Clear"
PCM_I2S_INTSTC_A_LABELS[3].comment = "RX Error Interrupt Status / Clear"
[setattr(PCM_I2S_INTSTC_A_LABELS[i], "mode", "W1C") for i in range(0, 4)]

PCM_I2S_GRAY_LABELS = \
[
    label("EN", 0, 0, "Enable GRAY Mode", "RW"),
    label("CLR", 1, 1, "Clear the GRAY Mode Logic", "RW"),
    label("FLUSH", 2, 2, "Flush the RX Buffer into the RX FIFO", "RW"),
    label("-", 3, 3, "Reserved", "-"),
    label("RXLEVEL", 4, 9, "The current fill level of the RX Buffer", "RO"),
    label("FLUSHED", 10, 15, "The number of bits that were flushed into the RX FIFO", "RO"),
    label("RXFIFOLEVEL", 16, 21, "The current level of the RX FIFO", "RO"),
    label("-", 22, 31, "Reserved", "-"),
]

PCM_I2S_CS_A     = labelbits(PCM_I2S_CS_A_LABELS)
PCM_I2S_FIFO_A   = labelbits(PCM_I2S_FIFO_A_LABELS)
PCM_I2S_MODE_A   = labelbits(PCM_I2S_MODE_A_LABELS)
PCM_I2S_RXC_A    = labelbits(PCM_I2S_TXC_A_RXC_A_LABELS)
PCM_I2S_TXC_A    = labelbits(PCM_I2S_TXC_A_RXC_A_LABELS)
PCM_I2S_DREQ_A   = labelbits(PCM_I2S_DREQ_A_LABELS)
PCM_I2S_INTEN_A  = labelbits(PCM_I2S_INTEN_A_LABELS)
PCM_I2S_INTSTC_A = labelbits(PCM_I2S_INTSTC_A_LABELS)
PCM_I2S_GRAY     = labelbits(PCM_I2S_GRAY_LABELS)

PCM_I2S_CS_A.info(     "PCM_I2S_CS_A",     0x002A6000) #0xFE203000
PCM_I2S_FIFO_A.info(   "PCM_I2S_FIFO_A",   0x0D408284) #0xFE203004
PCM_I2S_MODE_A.info(   "PCM_I2S_MODE_A",   0x00000000) #0xFE203008
PCM_I2S_RXC_A.info(    "PCM_I2S_RXC_A",    0x00000000) #0xFE20300c
PCM_I2S_TXC_A.info(    "PCM_I2S_TXC_A",    0x00000000) #0xFE203010
PCM_I2S_DREQ_A.info(   "PCM_I2S_DREQ_A",   0x10303020) #0xFE203014
PCM_I2S_INTEN_A.info(  "PCM_I2S_INTEN_A",  0x00000000) #0xFE203018
PCM_I2S_INTSTC_A.info( "PCM_I2S_INTSTC_A", 0x00000000) #0xFE20301C
PCM_I2S_GRAY.info(     "PCM_I2S_GRAY",     0x00000000) #0xFE203020
