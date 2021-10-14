class label:
    def __init__(self, name = "[LABEL]",
        shift = 0, mask = 0xFFFFFFFF, comment = "", mode = "", *args, **kwargs):
        self.name = name
        self.shift = shift
        self.mask = mask
        self.comment = comment
        self.mode = mode

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

    def info(self, header, binary, indent = 32, dashes = 64):
        print("---[" + header + "]" + ("-" * (dashes - len(header) - 5)) + "\n")
        raw = "{:032b}".format(binary)
        print(("Raw Data:\t").replace("\t", " " * (indent - 9)) + str(raw) + " [LSB]\n")
        for item in self.labels:
            data = (binary >> item.shift) & item.mask
            line = str(item.name) + ":\t" + self.cover(binary, item)
            comment = "//" + str(item.comment)
            print(comment + "\n" + line.replace("\t", " " * (indent - len(item.name) - 1)) + " [" + item.mode + "]\n")
        print(("-" * dashes) + "\n")

DMA4_11_CS_LABELS = \
[
    label("ACTIVE", 0, 0b1, "Activate the DMA4", "RW"),
    label("END", 1, 0b1, "End Flag", "W1C"),
    label("INT", 2, 0b1, "Interrupt Status", "W1C"),
    label("DREQ", 3, 0b1, "Data Request State", "RO"),
    label("RD_PAUSED", 4, 0b1, "DMA Read Paused State", "RO"),
    label("WR_PAUSED", 5, 0b1, "DMA Write Paused State", "RO"),
    label("DREQ_STOPS_DMA", 6, 0b1, "DMA Paused by DREQ State", "RO"),
    label("WAITING_FOR_OUTSTANDING_WRITES", 7, 0b1, "Waiting for outstanding writes", "RO"),
    label("-", 8, 0b11, "Reserved", "-"),
    label("ERROR", 10, 0b1, "DMA Error", "RO"),
    label("-", 11, 0b11111, "Reserved", "-"),
    label("QOS", 16, 0b1111, "AXI Quality of Service Level", "RW"),
    label("PANIC_QOS", 20, 0b1111, "AXI Panic Quality of Service Level", "RW"),
    label("DMA_BUSY", 24, 0b1, "Indicates the DMA4 is BUSY", "RO"),
    label("OUTSTANDING_TRANSACTIONS", 25, 0b1, "Outstanding AXI Transfers", "RO"),
    label("-", 26, 0b11, "Reserved", "-"),
    label("WAIT_FOR_OUTSTANDING_WRITES", 28, 0b1, "Wait for outstanding writes", "RW"),
    label("DISDEBUG", 29, 0b1, "Disable Debug Pause Signal", "RW"),
    label("ABORT", 30, 0b1, "Abort DMA Transfer", "W1SC"),
    label("HALT", 31, 0b1, "Halt DMA Transfer", "W1SC"),
]

DMA4_11_CB1_LABELS = \
[
    label("ADDR", 0, 0xFFFFFFFF, "Control Block Address in Memory (Low)", "RW"),
]

DMA4_11_CB2_LABELS = \
[
    label("ADDR", 0, 0xFFFFFFFF, "Control Block Address in Memory (High?)", "dma4"),
]

DMA4_11_DEBUG1_LABELS = \
[
    label("WRITE_ERROR", 0, 0b1, "Slave Write Response Error", "RC"),
    label("FIFO_ERROR", 1, 0b1, "FIFO Error", "RC"),
    label("READ_ERROR", 2, 0b1, "Slave Read Response Error", "RC"),
    label("READ_CB_ERROR", 3, 0b1, "Slave Read Response Error During Control Block Read", "RC"),
    label("-", 4, 0b1111, "Reserved", "-"),
    label("INT_ON_ERROR", 8, 0b1, "Interrupt on Error", "RW"),
    label("HALT_ON_ERROR", 9, 0b1, "Halt on Error", "RW"),
    label("ABORT_ON_ERROR", 10, 0b1, "Abort on Error", "RW"),
    label("DISABLE_CLK_GATE", 11, 0b1, "Disable Clock Gating Logic", "RW"),
    label("-", 12, 0b11, "Reserved", "-"),
    label("R_STATE", 14, 0b1111, "Read State Machine State", "RO"),
    label("W_STATE", 18, 0b1111, "Write State Machine State", "RO"),
    label("-", 22, 0b1, "Reserved", "-"),
    label("RESET", 23, 0b1, "Hard Reset DMA State Machine", "W1SC"),
    label("ID", 24, 0b1111, "Identification", "RO"),
    label("VERSION", 28, 0b1111, "Version", "RO"),
]

DMA4_11_TI_LABELS = \
[
    label("INTEN", 0, 0b1, "Interrupt Enable", "RW"),
    label("TDMODE", 1, 0b1, "2D Transfer Mode", "RW"),
    label("WAIT_RESP", 2, 0b1, "Wait for Write Response", "RW"),
    label("WAIT_RD_RESP", 3, 0b1, "Wait for Read Response", "RW"),
    label("-", 4, 0b11111, "Reserved", "-"),
    label("PERMAP", 9, 0b11111, "Peripheral Mapping", "RW"),
    label("S_DREQ", 14, 0b1, "Control Source Reads with DREQ", "RW"),
    label("D_DREQ", 15, 0b1, "Control Destination Writes with DREQ", "RW"),
    label("S_WAITS", 16, 0b11111111, "Read Wait Cycles", "RW"),
    label("D_WAITS", 24, 0b11111111, "Write Wait Cycles", "RW"),
]

DMA4_11_SRC_LABELS = \
[
    label("ADDR", 0, 0xFFFFFFFF, "Lower bits of the Source Address", "RW"),
]

DMA4_11_SRCI_LABELS = \
[
    label("ADDR", 0, 0b11111111, "High bits of the Source Address", "RW"),
    label("BURST_LENGTH", 8, 0b1111, "Burst Transfer Length", "RW"),
    label("INC", 12, 0b1, "Increment the Source Address", "RW"),
    label("SIZE", 13, 0b11, "Source Transfer Width", "RW"),
    label("IGNORE", 15, 0b1, "Ignore Reads", "RW"),
    label("STRIDE", 16, 0b1111111111111111, "Source Stride", "RW"),
]

DMA4_11_DEST_LABELS = \
[
    label("ADDR", 0, 0xFFFFFFFF, "Lower bits of the Destination Address", "RW"),
]

DMA4_11_DESTI_LABELS = \
[
    label("ADDR", 0, 0b11111111, "High bits of the Destination Address", "RW"),
    label("BURST_LENGTH", 8, 0b1111, "Burst Transfer Length", "RW"),
    label("INC", 12, 0b1, "Destination Address Increment", "RW"),
    label("SIZE", 13, 0b11, "Destination Transfer Width", "RW"),
    label("IGNORE", 15, 0b1, "Ignore Writes", "RW"),
    label("STRIDE", 16, 0b1111111111111111, "Destination Stride", "RW"),
]

DMA4_11_LEN_LABELS = \
[
    label("XLENGTH", 0, 0xFFFF, "Transfer Length in Bytes", "RW"),
    label("YLENGTH", 16, 0x3FFF, "2D Mode Number of XLENGTH Lines", "RW"),
    label("-", 30, 0b11, "Reserved", "-"),
]

DMA4_11_NEXT_CB_LABELS = \
[
    label("ADDR", 0, 0xFFFFFFFF, "Address of Next Control Block for Chained DMA Ops", "RW"),
]

DMA4_11_DEBUG2_LABELS = \
[
    label("OUTSTANDING_WRITES", 0, 0b111111111, "Outstanding Write Response Count", "RO"),
    label("-", 9, 0b1111111, "Reserved", "-"),
    label("OUTSTANDING_READS", 16, 0b111111111, "Outstanding Read Words Count", "RO"),
    label("-", 25, 0b1111111, "Reserved", "-"),
]

DMA_INT_STATUS_LABELS = \
[
    label("INT0", 0, 0b1, "Interrupt Status of DMA Engine 0", "RO"),
    label("INT1", 1, 0b1, "Interrupt Status of DMA Engine 1", "RO"),
    label("INT2", 2, 0b1, "Interrupt Status of DMA Engine 2", "RO"),
    label("INT3", 3, 0b1, "Interrupt Status of DMA Engine 3", "RO"),
    label("INT4", 4, 0b1, "Interrupt Status of DMA Engine 4", "RO"),
    label("INT5", 5, 0b1, "Interrupt Status of DMA Engine 5", "RO"),
    label("INT6", 6, 0b1, "Interrupt Status of DMA Engine 6", "RO"),
    label("INT7", 7, 0b1, "Interrupt Status of DMA Lite Engine 7", "RO"),
    label("INT8", 8, 0b1, "Interrupt Status of DMA Lite Engine 8", "RO"),
    label("INT9", 9, 0b1, "Interrupt Status of DMA Lite Engine 9", "RO"),
    label("INT10", 10, 0b1, "Interrupt Status of DMA Lite Engine 10", "RO"),
    label("INT11", 11, 0b1, "Interrupt Status of DMA4 Engine 11", "RO"),
    label("INT12", 12, 0b1, "Interrupt Status of DMA4 Engine 12", "RO"),
    label("INT13", 13, 0b1, "Interrupt Status of DMA4 Engine 13", "RO"),
    label("INT14", 14, 0b1, "Interrupt Status of DMA4 Engine 14", "RO"),
    label("INT15", 15, 0b1, "Interrupt Status of DMA VPU Engine 15", "RO"),
    label("-", 16, 0xFFFF, "Reserved", "-"),
]

DMA_ENABLE_LABELS = \
[
    label("EN0", 0, 0b1, "Enable DMA Engine 0", "RW"),
    label("EN1", 1, 0b1, "Enable DMA Engine 1", "RW"),
    label("EN2", 2, 0b1, "Enable DMA Engine 2", "RW"),
    label("EN3", 3, 0b1, "Enable DMA Engine 3", "RW"),
    label("EN4", 4, 0b1, "Enable DMA Engine 4", "RW"),
    label("EN5", 5, 0b1, "Enable DMA Engine 5", "RW"),
    label("EN6", 6, 0b1, "Enable DMA Engine 6", "RW"),
    label("EN7", 7, 0b1, "Enable DMA Lite Engine 7", "RW"),
    label("EN8", 8, 0b1, "Enable DMA Lite Engine 8", "RW"),
    label("EN9", 9, 0b1, "Enable DMA Lite Engine 9", "RW"),
    label("EN10", 10, 0b1, "Enable DMA Lite Engine 10", "RW"),
    label("EN11", 11, 0b1, "Enable DMA4 Engine 11", "RW"),
    label("EN12", 12, 0b1, "Enable DMA4 Engine 12", "RW"),
    label("EN13", 13, 0b1, "Enable DMA4 Engine 13", "RW"),
    label("EN14", 14, 0b1, "Enable DMA4 Engine 14", "RW"),
    label("-", 15, 0b111111111, "Reserved", "-"),
    label("PAGE", 24, 0b1111, "1GB SDRAM Page for DMA Engines 0-6", "RW"),
    label("PAGELITE", 28, 0b1111, "1GB SDRAM Page for DMA Lite Engines 7-10", "RW"),
]

DMA4_11_CS      = labelbits(DMA4_11_CS_LABELS)
DMA4_11_CB1     = labelbits(DMA4_11_CB1_LABELS)
DMA4_11_CB2     = labelbits(DMA4_11_CB2_LABELS)
DMA4_11_DEBUG1  = labelbits(DMA4_11_DEBUG1_LABELS)
DMA4_11_TI      = labelbits(DMA4_11_TI_LABELS)
DMA4_11_SRC     = labelbits(DMA4_11_SRC_LABELS)
DMA4_11_SRCI    = labelbits(DMA4_11_SRCI_LABELS)
DMA4_11_DEST    = labelbits(DMA4_11_DEST_LABELS)
DMA4_11_DESTI   = labelbits(DMA4_11_DESTI_LABELS)
DMA4_11_LEN     = labelbits(DMA4_11_LEN_LABELS)
DMA4_11_NEXT_CB = labelbits(DMA4_11_NEXT_CB_LABELS)
DMA4_11_DEBUG2  = labelbits(DMA4_11_DEBUG2_LABELS)

DMA_INT_STATUS  = labelbits(DMA_INT_STATUS_LABELS)
DMA_ENABLE      = labelbits(DMA_ENABLE_LABELS)

DMA4_11_CS.info(      "DMA4_11_CS_LABELS",      0x20000309) #0xFE007B00
DMA4_11_CB1.info(     "DMA4_11_CB1_LABELS",     0x00000000) #0xFE007B04
DMA4_11_CB2.info(     "DMA4_11_CB2_LABELS",     0x646D6134)
DMA4_11_DEBUG1.info(  "DMA4_11_DEBUG1_LABELS",  0x1B000400) #0xFE007B0C
DMA4_11_TI.info(      "DMA4_11_TI_LABELS",      0x00000001) #0xFE007B10
DMA4_11_SRC.info(     "DMA4_11_SRC_LABELS",     0x00000028) #0xFE007B14
DMA4_11_SRCI.info(    "DMA4_11_SRCI_LABELS",    0x00001006) #0xFE007B18
DMA4_11_DEST.info(    "DMA4_11_DEST_LABELS",    0x3EACB004) #0xFE007B1C
DMA4_11_DESTI.info(   "DMA4_11_DESTI_LABELS",   0x00001000) #0xFE007B20
DMA4_11_LEN.info(     "DMA4_11_LEN_LABELS",     0x00000000) #0xFE007B24
DMA4_11_NEXT_CB.info( "DMA4_11_NEXT_CB_LABELS", 0x00000000) #0xFE007B28
DMA4_11_DEBUG2.info(  "DMA4_11_DEBUG2_LABELS",  0x00000000) #0xFE007B2C

DMA_INT_STATUS.info(  "DMA_INT_STATUS_LABELS",  0x00000000) #0xFE007FE0
DMA_ENABLE.info(      "DMA_ENABLE_LABELS",      0x00007FFF) #0xFE007FF0
