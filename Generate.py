import re
from Defines import TesterResource,Units,APU12Range,PinMode,PINS,AttributeDefine
from UserFunction import AutomaticRange,ValueAutomaticSet
from datetime import datetime
class PaperWirte:
    def __init__(self,filename):
        self.file = open(filename,"w")
    def WriteLine(self,Words):
        self.file.writelines(Words + "\n")
    def Write(self,Words):
        self.file.write(Words)

# class Unit:
#     def __init__(self):
#         self

class Attribute:
    def __init__(self,ATTR_STR):
        if ATTR_STR == "" or ATTR_STR is None:
            self.dict = AttributeDefine.PrimaryForceVoltCurrentAttriDict
        else:
            self.dict = AttributeDefine.PrimaryForceVoltCurrentAttriDict
            ATTR_STR = ATTR_STR.lower().replace(" ","").split(",")
            for var in ATTR_STR:
                var = var.split(":")
                if var[0] in AttributeDefine.PrimaryForceVoltCurrentAttriDict:
                    if var[0] == "vrange":
                        if var[1] == "3.6v":
                            pass
                        elif var[1] == "10v":
                            self.dict["vrange"] = APU12Range.Vranges.APU12_10V
                        else:
                            self.dict["vrange"] = APU12Range.Vranges.APU12_30V
                    elif var[0] == "irange":
                        if var[1] == "1ma":
                            pass
                        elif var[1] == "10ma":
                            self.dict["irange"] = APU12Range.Iranges.APU12_10MA
                        elif var[1] == "10ua":
                            self.dict["irange"] = APU12Range.Iranges.APU12_10UA
                        elif var[1] == "100ma":
                            self.dict["irange"] = APU12Range.Iranges.APU12_100MA
                        elif var[1] == "100ua":
                            self.dict["irange"] = APU12Range.Iranges.APU12_100UA
                        else:
                            self.dict["irange"] = APU12Range.Iranges.APU12_200MA
                    elif var[0] == "caploadtime":
                        pass
                    elif var[0] == "forcerecord":
                        self.dict["forcerecord"] = var[1]
                    elif var[0] == "measurerecord":
                        self.dict["measurerecord"] = var[1]
                    elif var[0] == "target":
                        self.dict["target"] = var[1]
                    elif var[0] == "delay":
                        self.dict["delay"] = ValueAutomaticSet(var[1])
        # self.R = f"{0}{Units.ohm}"
        # self.H = f"{3.3}{Units.V}"
        # self.L = f"{0}{Units.V}"
        # self.D = f"{50}{Units.Per}"
        # self.T = f"{0}{Units.nS}"
        # self.step = f"{1}{Units.mV}"
        # self.value = None
        # self.steptime = f"{10}{Units.uS}"
        # self.target = None
        # self.record = None
        #
        # class Type:
        #     Edge1 = "R"
        #     Edge2 = "F"
        #     x1 = None
        #     x2 = None
        #     y1 = None
        #     y2 = None
        # self.type = {Type.Edge1:[Type.x1,Type.x2], Type.Edge2:[Type.y1,Type.y2]}
        #
        # self.slop = Units.POS
        # self.unit = None
        # self.vrange = APU12Range.Vranges.APU12_3p6V
        # self.irange = APU12Range.Iranges.APU12_10MA
        # self.dealy = f"{0}{Units.uS}"
        # self.cap = f"{0}{Units.uF}"
        # self.Kelvin = False
        #
        # self.ForceRecord = [""]
        # self.MeasureRecord = [""]
        #
        # self.CaploadTime = None
    # def AddAttribute(self,ATR):
    #     for var in ATR
class Generate:
    def __init__(self):
        super().__init__()
        self.PaW = PaperWirte("test.cpp")

    def FV(self,PINSTR,Forcevalue,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        VRange = ATTRobj.dict["vrange"]
        IRange = ATTRobj.dict["irange"]
        CaploadTime = ATTRobj.dict["caploadtime"]
        ForceRecord = ATTRobj.dict["forcerecord"]
        Delay = ATTRobj.dict["delay"]
        #判断 自定义范围是否合理
        if VRange not in APU12Range.ValidVranges and IRange not in APU12Range.ValidIranges:
            print(f"no support range {ATTRobj.dict['vrange']} {ATTRobj.dict['irange']}")
            return
        else:
            VRange = AutomaticRange("Volt",Forcevalue)
        #DFT AUTO Gen log
        self.PaW.WriteLine(f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:FV VALUE:{Forcevalue}")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        #针对单个pin
        if PINobj.pinmode == PinMode.single:
            if CaploadTime is None:
                self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                self.PaW.WriteLine(f"apu12setcapload({PINSTR}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if Delay is not None:self.PaW.WriteLine(f"lwait({Delay});")
            if ForceRecord is not None:self.PaW.WriteLine(f"{ForceRecord.upper()} = {Forcevalue};//FV ForceRecord")
        #针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            if CaploadTime is None:
                for pin in PINobj.contant:
                    self.PaW.WriteLine(f"apu12set({pin}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                for pin in PINobj.contant:
                    self.PaW.WriteLine(f"apu12setcapload({pin}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if Delay is not None:self.PaW.WriteLine(f"lwait({Delay});")
            if ForceRecord is not None:self.PaW.WriteLine(f"{ForceRecord.upper()} = {Forcevalue};//FV ForceRecord")
        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            print(f"FV:{PINSTR} ----error:no support PinMode.separate")
            return
        self.PaW.WriteLine(f"--------------------------------------------------------------------------------------------")
    def FI(self,PINSTR,Forcevalue,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        VRange = ATTRobj.dict["vrange"]
        IRange = ATTRobj.dict["irange"]
        CaploadTime = ATTRobj.dict["caploadtime"]
        ForceRecord = ATTRobj.dict["forcerecord"]
        Delay = ATTRobj.dict["delay"]
        #判断 自定义范围是否合理
        if VRange not in APU12Range.ValidVranges and IRange not in APU12Range.ValidIranges:
            print(f"no support range {VRange} {IRange}")
            return
        else:
            IRange = AutomaticRange("Current",Forcevalue)
        #DFT AUTO Gen log
        self.PaW.WriteLine(f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:FV VALUE:{Forcevalue}")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        # 针对单个pin
        if PINobj.pinmode == PinMode.single:
            if CaploadTime is None:
                self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                self.PaW.WriteLine(f"apu12setcapload({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if Delay is not None:self.PaW.WriteLine(f"lwait({Delay});")
            if ForceRecord is not None:self.PaW.WriteLine(f"{ForceRecord.upper()} = {Forcevalue};//FI ForceRecord")
        # 针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            if CaploadTime is None:
                for pin in PINobj.contant:
                    self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                for pin in PINobj.contant:
                    self.PaW.WriteLine(f"apu12setcapload({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if Delay is not None:self.PaW.WriteLine(f"lwait({Delay});")
            if ForceRecord is not None:self.PaW.WriteLine(f"{ForceRecord.upper()} = {Forcevalue};//FI ForceRecord")
        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            print(f"FI:{PINSTR} ----error:no support PinMode.separate")
            return
        self.PaW.WriteLine(f"--------------------------------------------------------------------------------------------")
    def FIMV(self,PINSTR,Forcevalue,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        VRange = ATTRobj.dict["vrange"]
        IRange = ATTRobj.dict["irange"]
        CaploadTime = ATTRobj.dict["caploadtime"]
        ForceRecord = ATTRobj.dict["forcerecord"]
        MeasureRecord = ATTRobj.dict["measurerecord"]
        Delay = ATTRobj.dict["delay"]
        # 判断 自定义范围是否合理
        if IRange not in APU12Range.ValidIranges and VRange not in APU12Range.ValidVranges:
            print(f"no support range {IRange}")
            return
        else:
            IRange = AutomaticRange("Current",Forcevalue)
        # DFT AUTO Gen log
        self.PaW.WriteLine(f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:FIMV VALUE:{Forcevalue}")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        # 针对单个pin
        if PINobj.pinmode == PinMode.single:
            if CaploadTime is None:
                self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                self.PaW.WriteLine(f"apu12setcapload({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if Delay is not None: self.PaW.WriteLine(f"lwait({Delay});")
            if ForceRecord is not None:self.PaW.WriteLine(f"{ForceRecord} = {Forcevalue};//FIMV ForceRecord")
            self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mv({PINSTR}, 4000, 13.0);")
            self.PaW.WriteLine(f"apu12mv({PINSTR}, 20, 13.0);")
            self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
            if MeasureRecord is not None: self.PaW.WriteLine(f"groupgetresults({MeasureRecord.upper()}, NUM_SITES);//FIMV MeasureRecord")
            self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FI, 0, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FI, 0, {VRange}, {IRange}, APU12_PIN_TO_VI);")  # off
        #针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            print(f"FIMV:{PINSTR} ----error:no support PinMode.synchronous")
            return
        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            self.PaW.WriteLine(f"OPERATE_PINS.clear();")  # This should be Defined at the begining of Function
            for pin in PINobj.contant:self.PaW.WriteLine(f"OPERATE_PINS.pushback({pin});")
            self.PaW.WriteLine("for (int i = 0; i < OPERATE_PINS.size(); i++)\n{")
            if CaploadTime is None:
                self.PaW.WriteLine(f"    apu12set(OPERATE_PINS[i], APU12_FI, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            else:
                self.PaW.WriteLine(f"    apu12setcapload({PINSTR}, APU12_FI, {Forcevalue}, {VRange}, {IRange}, {CaploadTime}, APU12_PIN_TO_VI);")
            if ForceRecord is not None:self.PaW.WriteLine(f"    {ForceRecord.upper()} = {Forcevalue};//FIMV ForceRecord")
            self.PaW.WriteLine(f"    lwait(100);")
            self.PaW.WriteLine(f"    if (debug_wait_num == indexOfTest) apu12mv(OPERATE_PINS[i], 4000, 13.0);")
            self.PaW.WriteLine(f"    apu12mv(OPERATE_PINS[i], 20, 13);")
            self.PaW.WriteLine(f"    groupgetresults(results[indexOfTest], NUM_SITES);")
            if MeasureRecord is not None:self.PaW.WriteLine(f"    groupgetresults({MeasureRecord.upper()}, NUM_SITES);//FIMV MeasureRecord")
            self.PaW.WriteLine(f"    apu12set(OPERATE_PINS[i], APU12_FI, 0, {VRange}, {IRange}, APU12_PIN_TO_VI);")
            self.PaW.WriteLine(f"    apu12set(OPERATE_PINS[i], APU12_OFF, 0, {VRange}, {IRange}, APU12_PIN_TO_VI);//off")
            self.PaW.WriteLine("    lwait(100);\n}")
        self.PaW.WriteLine(f"--------------------------------------------------------------------------------------------")
    def FVpull(self,PINSTR,Forcevalue,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        VRange = ATTRobj.dict["vrange"]
        IRange = ATTRobj.dict["irange"]
        Delay = ATTRobj.dict["delay"]
        # 判断 自定义范围是否合理
        if IRange not in APU12Range.ValidIranges and VRange not in APU12Range.ValidVranges:
            print(f"no support range {IRange}")
            return
        else:
            VRange = AutomaticRange("Volt",Forcevalue)
        # DFT AUTO Gen log
        self.PaW.WriteLine(
            f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:FVPULL VALUE:{Forcevalue}")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        # 针对单个pin
        if PINobj.pinmode == PinMode.single:
            self.PaW.WriteLine(f"Relay(K_{PINSTR}_PULL, K_CLOSE);")
            self.PaW.WriteLine(f"lwait(3500);")
            self.PaW.WriteLine(f"apu12set({PINSTR}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
        #针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            for pin in PINobj.contant: self.PaW.WriteLine(f"Relay(K_{pin}_PULL, K_CLOSE);")
            self.PaW.WriteLine(f"lwait(3500);")
            self.PaW.Write(f"apu12set(")
            for pin in PINobj.contant:
                self.PaW.Write(f"{pin}_")
            self.PaW.Write(f"PULL, APU12_FV, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);\n")

        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            for pin in PINobj.contant: self.PaW.WriteLine(f"Relay(K_{pin}_PULL, K_CLOSE);")
            self.PaW.WriteLine(f"lwait(3500);")
            for pin in PINobj.contant:self.PaW.WriteLine(f"apu12set({pin}, APU12_FV, {Forcevalue}, {VRange}, {IRange}, APU12_PIN_TO_VI);")
        if Delay is not None: self.PaW.WriteLine(f"lwait({Delay});")
    def FVfreq(self):
        pass

    def FVdelta(self):
        pass

    def FIdelta(self):
        pass

    def FVpulse(self):
        pass

    def FIpulse(self):
        pass

    def FVjump(self):
        pass

    def FIjump(self):
        pass

    def FIramp(self):
        pass

    def MV(self,PINSTR,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        MeasureRecord = ATTRobj.dict["measurerecord"]
        # DFT AUTO Gen log
        self.PaW.WriteLine(f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:MV")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        # 针对单个pin
        if PINobj.pinmode == PinMode.single:
            self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mv({PINSTR}, 4000, 13.0);")
            self.PaW.WriteLine(f"apu12mv({PINSTR}, 20, 13);")
            self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
            if MeasureRecord is not None:self.PaW.WriteLine(f"groupgetresults({MeasureRecord.upper()}, NUM_SITES);//MV MeasureRecord")
        # 针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            for pin in PINobj.contant:
                self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mv({pin}, 4000, 13.0);")
                self.PaW.WriteLine(f"apu12mv({pin}, 20, 13);")
                self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            for pin in PINobj.contant:
                self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mv({pin}, 4000, 13.0);")
                self.PaW.WriteLine(f"apu12mv({pin}, 20, 13);")
                self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
        self.PaW.WriteLine(f"--------------------------------------------------------------------------------------------")

    def MI(self,PINSTR,ATTR_STR=None):
        # 根据PINSTR 选择force模式
        PINobj = PINS(PINSTR)
        # 属性解析
        ATTRobj = Attribute(ATTR_STR)
        MeasureRecord = ATTRobj.dict["measurerecord"]
        # DFT AUTO Gen log
        self.PaW.WriteLine(
            f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: PINS:{PINSTR} OPERATE:MV")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        # 针对单个pin
        if PINobj.pinmode == PinMode.single:
            self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mi({PINSTR}, 4000, 13.0);")
            self.PaW.WriteLine(f"apu12mi({PINSTR}, 20, 13);")
            self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
            if MeasureRecord is not None:self.PaW.WriteLine(f"groupgetresults({MeasureRecord.upper()}, NUM_SITES);//MI MeasureRecord")
        # 针对多个pin同时
        elif PINobj.pinmode == PinMode.synchronous:
            for pin in PINobj.contant:
                self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mi({pin}, 4000, 13.0);")
                self.PaW.WriteLine(f"apu12mi({pin}, 20, 13);")
                self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
        # 针对多个pin分开
        elif PINobj.pinmode == PinMode.separate:
            for pin in PINobj.contant:
                self.PaW.WriteLine(f"if (debug_wait_num == indexOfTest) apu12mi({pin}, 4000, 13.0);")
                self.PaW.WriteLine(f"apu12mi({pin}, 20, 13);")
                self.PaW.WriteLine(f"groupgetresults(results[indexOfTest], NUM_SITES);")
        self.PaW.WriteLine(
            f"--------------------------------------------------------------------------------------------")
    def MVfreq(self):
        pass

    def MVperiod(self):
        pass

    def MVdelta(self):
        pass

    def MIdelta(self):
        pass

    def MVTpulse(self):
        pass

    def MVTjump(self):
        pass

    def MVflip(self):
        pass

    def MIflip(self):
        pass

    def MVTdelay(self):
        pass

    def Read(self):
        pass

    def Calculate(self,ResultSTR,Fomula,ATTR_STR=None):
        # # 属性解析
        # ATTRobj = Attribute(ATTR_STR)
        # Unit = ATTRobj.dict["unit"]
        Fomulaobj = re.split(r'([+\-*/])', Fomula)
        Fomulaobj = [item for item in Fomulaobj if item]
        # DFT AUTO Gen log
        self.PaW.WriteLine(
            f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen: OPERATE:Calculate CalculateFomula:{ResultSTR}={Fomula}")
        self.PaW.WriteLine(f"//-----Attribute:{ATTR_STR}")
        self.PaW.WriteLine(f"groupgetresults({ResultSTR}, NUM_SITES);//There might be a problem")
        self.PaW.WriteLine("FOR_EACH_SITE(site, NUM_SITES)\n{")
        self.PaW.Write(f"    {ResultSTR}[site].value = ")
        for var in Fomulaobj:
            if re.search(r'[a-zA-Z]', var) is not None:
                self.PaW.Write(f"{var}[site].value ")
            else:
                self.PaW.Write(f"{var} ")
        self.PaW.WriteLine("\n}")
        self.PaW.WriteLine(
            f"--------------------------------------------------------------------------------------------")