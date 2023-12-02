from Generate import Generate
from Defines import Units ,PINS
# class Main:
#     def __init__(self):
#         self.Gen = Generate
#         self.Gen.ForeceVolt(Pins="AP_VCC",Value=-2,Units=TesterUnits.V,Range="APU12_10V")


if __name__ == "__main__":
    Gen = Generate()
    # #测试
    # #属性中挡位带来的优先级低于自动挡位优先级
    # Gen.FV("EN1",3.3,"vRange:10V,irange:10uA,forcerecord:V1")
    # Gen.FV("EN2", 3.3, "vrange:10V,irange:10uA,forcerecord:V2")
    #
    # Gen.FI("FLT#_MF1", 4)
    #
    # Gen.FIMV("PWM8_1/PWM7_2/PWM6_3/PWM5_4/PWM4_5/PWM3_6/PWM2_7/PWM1_8",4,"vrange:3.6V, irange:100uA,MeasUrerecord:V10, forcerecord:I1")
    #
    #
    # Gen.MV("EN1","MeasUrerecord:V3")
    # Gen.MV("EN1", "MeasUrerecord:V4")
    # Gen.Calculate("Ratio","V2/2*V3-0.2")
    Gen.FVpull("EN1|EN2",3.3,"delay:3600US")