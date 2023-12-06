import pandas as pd
import numpy as np
import re ,os
from UserFunction import ValueAutomaticSet,CurrentFunctionName,GenConsoleLog,LogLevel
from Generate import Generate
from Defines import  ValidOperations
from datetime import datetime
class DFT_File_Interaction:
    def __init__(self):
        super().__init__()
        self.__dftfile = None
        self.__df = None
        # self.Test_Procedure = None
        # self.Test_Name = None
        # self.Command = None
        # self.Part_Number = None
        self.DFT_Operation_Dict = {}
    def OpenDFT(self,filepath):
        self.__dftfile = filepath
        if os.path.exists(filepath):
            self.__df = pd.read_excel(filepath, sheet_name=' {Output}')#for now try [Output] sheet
        else:
            raise f"In DFT_File_Interaction--- OpenDFT:{filepath} not exists!!!"
    def DFTRead(self):
        Test_Procedure = self.__df['Test Procedure']
        Test_Name = self.__df['Test Name']
        Command = self.__df['Command']
        Part_Number = self.__df['Applicable Part']
        pattern = r'《(.*?):(.*?)=(.*?)<(.*?)>》'

        index_Name = Test_Name[~Test_Name.isnull()].index.tolist()
        name_tolist = Test_Name[index_Name]

        index_part = Part_Number[~Part_Number.isnull()].index.tolist()
        part_tolist = Part_Number[index_part]

        Index_name = name_tolist.index
        # dict = {}
        # len(Index_name)-1
        for i in range(3):
            TestName_start = int(Index_name[i])
            TestName_end = int(Index_name[i + 1])
            PartNumber_List = pd.DataFrame(Part_Number.iloc[TestName_start:TestName_end].unique()).dropna().values.tolist()
            # 所有part相同的测试项
            if len(PartNumber_List) == 1:
                PartNumber_start = TestName_start
                PartNumber_end = TestName_end
                matches = []
                for j in range(PartNumber_start, PartNumber_end):
                    origncellstr = Test_Procedure.iloc[j]
                    match = re.findall(pattern, origncellstr)
                    if match:
                        match = [list(i) for i in match]
                        # match[0][2] = StrOperate(match[0][2]).remove_letters()
                        match[0][2] = ValueAutomaticSet(match[0][2])
                        # print(match[0][2])
                        matches.extend(match)
                    else:
                        if Command.iloc[j] is None or Command.iloc[j] == "":
                            GenConsoleLog(CurrentFunctionName(),"No Dig CMD !!!")
                        matches.append(["DigCMD", Command.iloc[j]])
                dict = {name_tolist.iloc[i]: {tuple(PartNumber_List[-1]): matches}}
                self.DFT_Operation_Dict.update(dict)
            # 同一个测试项，不同part不同的测试方法
            elif len(PartNumber_List) > 1:
                dict_temp = {}
                for k in range(len(PartNumber_List) - 1):
                    PartNumber_start = Part_Number.iloc[TestName_start:TestName_end][
                    Part_Number.iloc[TestName_start:TestName_end].values == PartNumber_List[k]].index
                    PartNumber_start = int(PartNumber_start[0])
                    PartNumber_end = Part_Number.iloc[TestName_start:TestName_end][
                    Part_Number.iloc[TestName_start:TestName_end].values == PartNumber_List[k + 1]].index
                    PartNumber_end = int(PartNumber_end[0])
                    matches = []
                    for l in range(PartNumber_start, PartNumber_end):
                        origncellstr = Test_Procedure.iloc[l]
                        match = re.findall(pattern, origncellstr)
                        if match:
                            match = [list(i) for i in match]
                            match[0][2] = ValueAutomaticSet(match[0][2])
                            matches.extend(match)
                        else:
                            if Command.iloc[l] is None or Command.iloc[l] == "":
                                GenConsoleLog(CurrentFunctionName(),"No Dig CMD !!!")
                            matches.append(["DigCMD",Command.iloc[l]])
                    dict_1 = {tuple(PartNumber_List[k]): matches}
                    dict_temp.update(dict_1)
                PartNumberLast_start = Part_Number.iloc[TestName_start:TestName_end][
                Part_Number.iloc[TestName_start:TestName_end].values == PartNumber_List[-1]].index
                PartNumberLast_start = int(PartNumberLast_start[0])
                PartNumberLast_end = TestName_end
                matches = []
                for m in range(PartNumberLast_start, PartNumberLast_end):
                    origncellstr = Test_Procedure.iloc[m]
                    match = re.findall(pattern, origncellstr)
                    if match:
                        match = [list(i) for i in match]
                        match[0][2] = ValueAutomaticSet(match[0][2])
                        matches.extend(match)
                    else:
                        if Command.iloc[m] is None or Command.iloc[m] == "":
                            GenConsoleLog(CurrentFunctionName(), "No Dig CMD !!!")
                        matches.append(["DigCMD", Command.iloc[m]])
                dict_1 = {tuple(PartNumber_List[-1]): matches}
                dict_temp.update(dict_1)
                dict = {name_tolist.iloc[i]: dict_temp}
                self.DFT_Operation_Dict.update(dict)
            # part cell is empty
            else:
                print('Partnumber does not exist')

    def DFT_Generate(self):
        GenOBJ = Generate()
        GenOBJ.TestFunctionSetup()
        for key1 , value1 in self.DFT_Operation_Dict.items():
            GenOBJ.PaW.WriteLine(f"//-------------------->TestItem:{key1} start")
            for key2, value2 in value1.items():
                PartList = key2[0].replace(",","").replace(" ","").split("\n")
                GenOBJ.PaW.WriteLine(f"//-------------->Part:{PartList} start")
                GenOBJ.PaW.Write(f'if (')
                if len(PartList) > 1:
                    for index in range(len(PartList)):
                        if index == len(PartList) -1:
                            GenOBJ.PaW.Write(f" ThisProduct == {PartList[index]})\n{{\n")
                        else:
                            GenOBJ.PaW.Write(f" ThisProduct == {PartList[index]}) ||")
                else:
                    GenOBJ.PaW.Write(f"ThisProduct == {PartList[0]})\n{{\n")
                #print(f"TestItem:{key1}---Part:{key2}  Operations:{value2}")
                if 'PMBUS' in key2:
                    GenOBJ.PaW.WriteLine(value2)
                else:
                    for operatestr in value2:
                        operate = operatestr[0].lower()
                        if operate in ValidOperations:
                            if operate == 'fv':
                                GenOBJ.FV(operatestr[1],operatestr[2],operatestr[3])
                            elif operate == 'fi':
                                GenOBJ.FI(operatestr[1],operatestr[2],operatestr[3])
                            elif operate == 'mv':
                                GenOBJ.MV(operatestr[1],operatestr[2])
                            elif operate == 'mi':
                                GenOBJ.MI(operatestr[1], operatestr[2])
                            elif operate == 'fimv':
                                GenOBJ.FIMV(operatestr[1], operatestr[2], operatestr[3])
                            # elif operate == 'fvmi':
                            #     # GenOBJ.FVMI(value2[1], value2[2], value2[3])
                            elif operate == 'fvpull':
                                GenOBJ.FVpull(operatestr[1], operatestr[2])
                            elif operate == 'calcualte':
                                GenOBJ.Calculate(operatestr[1],operatestr[2],operatestr[3])
                            elif operate == 'digcmd':
                                # DFT AUTO Gen log
                                GenOBJ.PaW.WriteLine(
                                    f"//-----[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DFT AUTO Gen:  OPERATE:DigCMD for {key1}")
                                GenOBJ.PaW.WriteLine(f"{operatestr[1]}")
                                # GenOBJ.PaW.WriteLine(
                                #     f"--------------------------------------------------------------------------------------------")
                        else:
                            GenConsoleLog(CurrentFunctionName(), f"TestItem:{key1}---Part:{key2} Operation:{operate} InValid!!!",LogLevel.Error)
                GenOBJ.PaW.Write(f'}}\n')
                GenOBJ.PaW.WriteLine(f"//-------------->Part:{PartList} end\n")
                GenConsoleLog(CurrentFunctionName(), f"TestItem:{key1}---Part:{key2} fine")

            GenOBJ.PaW.WriteLine(f"//-------------------->TestItem:{key1} end\n\n")
        GenOBJ.TestFunctionEnd()