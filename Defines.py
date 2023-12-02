class TesterResource:
    #ETS88
    APU12 = 1
    SPU112 = 2
    DPU16 = 3

    #Other
class APU12Range:
    class Vranges:
        APU12_3p6V = "APU12_3p6V"
        APU12_10V = "APU12_10V"
        APU12_30V = "APU12_30V"
    class Iranges:
        APU12_10UA = "APU12_10UA"
        APU12_100UA = "APU12_100UA"
        APU12_1MA = "APU12_1MA"
        APU12_10MA = "APU12_10MA"
        APU12_100MA = "APU12_100MA"
        APU12_200MA = "APU12_200MA"
    ValidVranges = ("APU12_3p6V","APU12_10V","APU12_30V")
    ValidIranges = ("APU12_10UA", "APU12_100UA", "APU12_1MA","APU12_10MA","APU12_100MA","APU12_200MA")
    # vranges = {
    #     APU12_3p6V:"APU12_3p6V"
    # }

class AttributeDefine:
    # ValidAttribute = ["vrange","irange","value","forcerecord","measurerecord","caploadtime"]
    PrimaryForceVoltCurrentAttriDict = {
        "vrange":APU12Range.Vranges.APU12_3p6V,
        "irange":APU12Range.Iranges.APU12_1MA,
        "caploadtime":None,
        "target":None,
        "measurerecord":None,
        "forcerecord":None,
        "delay":None,
        "unit":None
    }

class Units:
    #Volt
    V = "v"
    mV = "mv"
    uV = "uv"

    #Current
    A = "a"
    mA = "ma"
    uA = "ua"
    nA = "na"

    #Time
    nS = "ns"
    mS = "ms"
    uS = "us"
    S = "s"

    #Frequency
    Hz = "hz"
    KHz = "khz"
    MHz = "mhz"

    #resistance
    ohm = "ohm"
    Kohm = "kohm"
    Mohm = "mohm"

    #capacitance
    nF = "nf"
    uF = "uf"
    pF = "pf"


    #other
    POS = "pos"
    NEG = "neg"
    Per = "%"

class PinMode:
        single = "single"
        synchronous = "synchronous"
        separate = "separate"

class PINS:
    def __init__(self,PIN_STR):
        if "|" in PIN_STR:
            self.pinmode = PinMode.synchronous
            self.contant = PIN_STR.split("|")
        elif "/" in PIN_STR:
            self.pinmode = PinMode.separate
            self.contant = PIN_STR.split("/")
        else:
            self.pinmode = PinMode.single
            self.contant = PIN_STR

Sequence = ["FV",]

