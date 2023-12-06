import re
from Defines import APU12Range,Units,LogLevel
import inspect
from datetime import datetime
class StrOperate:
    def __init__(self):
        pass
    def remove_digits_and_decimal(self,text):
        return re.sub(r'\d|\.', '', text)

    def remove_letters(self,text):
        return re.sub(r'[a-zA-Z]', '', text)

def AutomaticRange(Mode, Value):
    Value = abs(Value)
    if Mode == "Volt":
        if Value < 3.6:
            return APU12Range.Vranges.APU12_3p6V
        elif 3.6 < Value < 10:
            return APU12Range.Vranges.APU12_10V
        else:
            return APU12Range.Vranges.APU12_30V
    elif Mode == "Current":
        if Value < 0.01:
            return APU12Range.Iranges.APU12_10UA
        elif 0.01 <= Value < 0.1:
            return APU12Range.Iranges.APU12_100UA
        elif 0.1 <= Value < 1:
            return APU12Range.Iranges.APU12_1MA
        elif 1 <= Value < 10:
            return APU12Range.Iranges.APU12_10MA
        elif 10 <= Value < 100:
            return APU12Range.Iranges.APU12_100MA
        else:
            return APU12Range.Iranges.APU12_200MA
    else:
        print(f"错误的AutomaticRange调用 ---{Mode} {Value}")
        return

def ValueAutomaticSet(ValueStr):
    #单位
    unit = re.sub(r'[-.\d]+', '', ValueStr).lower()
    #值
    if '.' in ValueStr:
        value = float(re.sub(r'[a-zA-Z]', '', ValueStr))
    else:
        value = int(re.sub(r'[a-zA-Z]', '', ValueStr))
    if value is None:
        return None
    if unit is None:
        return value
    if "v" in unit:
        if unit == Units.V:
            return value
        elif unit == Units.mV:
            return value/1000
        elif unit == Units.uV:
            return value/1000000
    elif "a" in unit:
        if unit == Units.mA:
            return value
        elif unit == Units.A:
            return value*1000
        elif unit == Units.uA:
            return  value/1000
        elif unit == Units.nA:
            return value/1000000
    elif "s" in unit:
        if unit == Units.uS:
            return value
        elif unit == Units.mS:
            return value*1000
    else:
        print(f"no support  -- {ValueStr}")

def CurrentFunctionName():
    frame = inspect.currentframe().f_back
    return frame.f_code.co_name

def GenConsoleLog(where,logstr,loglevel = LogLevel.Normal):
    print(f"[{loglevel}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}---On[{where}]--->{logstr}")

