DEBUG = False

if DEBUG:
    import EquationStuff
    import VariableStuff
else:
    from mini_garedami import EquationStuff
    from mini_garedami import VariableStuff

ANS = dict()
MAX_TEST = 0

def str2CppCmp(x:str) -> list():
    res = []
    x = x.replace("\r","").split("\n")
    for e in x:
        for f in e.strip().split(" "):
            if f.strip():
                res.append(f.strip())
    
    return res

def readSolution(refAns):
    #read solution...
    global ANS,MAX_TEST

    ANS = dict()


    #split line and ';' to content
    lines = refAns.strip().replace("\r","").split("\n")
    content = []
    for line in lines:
        content.extend(line.strip().split(";"))


    
    for chunk in content:
        #Convert chunk to mini-chunk data
        #V1 = 2 A to ['V1','=','2','A']
        data = str2CppCmp(chunk.strip())

        #if data has '=' in second 
        #That mean variable compare
        if data[1] == '=':
            if len(data[-1]) > 2:
                print("refAns Error : Wrong unit in variable {}".format(data[0]))
                continue
            
            solAnswer = VariableStuff.ComplexNumber.fromStr(' '.join(data[2:-1]))
            
            if type(solAnswer) == "hello":
                print("refAns Error :in variable {} Can't convert {} to (Complex) number ({})".format(data[0],' '.join(data[2:-1]), solAnswer))
                continue

            if len(data[-1]) == 2:
                if not (data[-1][0] in "EPTGMkmunpfa"):
                    print("refAns Error :in variable {} Wrong prefix".format(data[0],data[-1]))
                    continue
                
                if data[-1][0] == 'E':
                    solAnswer *= 1e18
                elif data[-1][0] == 'P':
                    solAnswer *= 1e15
                elif data[-1][0] == 'T':
                    solAnswer *= 1e12
                elif data[-1][0] == 'G':
                    solAnswer *= 1e9
                elif data[-1][0] == 'M':
                    solAnswer *= 1e6
                elif data[-1][0] == 'k':
                    solAnswer *= 1e3
                elif data[-1][0] == 'm':
                    solAnswer *= 1e-3
                elif data[-1][0] == 'u':
                    solAnswer *= 1e-6
                elif data[-1][0] == 'n':
                    solAnswer *= 1e-9
                elif data[-1][0] == 'p':
                    solAnswer *= 1e-12
                elif data[-1][0] == 'f':
                    solAnswer *= 1e-15
                elif data[-1][0] == 'a':
                    solAnswer *= 1e-18
            #add to ANS
            ANS[data[0]] = (solAnswer,data[-1][-1])

        #if data ':' in second 
        #That mean Equation Compare
        elif data[1] == ':':
            #if return in str that mean Equation Error
            result = EquationStuff.convertAndCheck(" ".join(data[2:]))
            if type(result) == type("hello"):
                print("refAns Error : in Equation {} Err ({})".format(data[0],result))
                continue
            else:
                ANS[data[0]] = " ".join(data[2:])
            
        
    
    MAX_TEST = len(ANS)




def grading(student_out:str, ref_ans:str, fullscore, report, attrib, neg_handling=True):
    global ANS,MAX_TEST
    tol = float(attrib)

    def reportFormatError(content):
        #Student Format Error
        #If you have some report level you can put it here
        print(content)

    
    def reportWrongAnswer(content):
        if report != "HidNum":
            print(content)
    
    studentOutLines = student_out.strip().split('\n')
    refAnsLines = ref_ans.strip().split('\n')
    useLine = 0
    correct = 0
    
    for lineI,refline in enumerate(refAnsLines):
        judged = set()
        perfect = True
    
        readSolution(refline)
        if MAX_TEST == 0:
            print("Warning : No test in line {} ({})".format(lineI+1,refline))
            continue
        useLine += 1


        studentContent = studentOutLines[lineI].split(';')
        

        for chunk in studentContent:
            #Convert chunk to mini-chunk data
            #V1 = 2 A to ['V1','=','2','A']
            data = str2CppCmp(chunk.strip())

            if data[0] in ANS and data[0] not in judged:
                if data[1] == '=':
                    if type(ANS[data[0]]) == type(tuple()):

                        if data[-1][-1] != ANS[data[0]][1]:
                            reportFormatError("{} : Wrong Unit (Expect {} but got {}).".format(data[0], ANS[data[0]][1], data[-1][-1]))
                            perfect = False
                            judged.add(data[0])
                            continue

                        userAnswer = VariableStuff.ComplexNumber.fromStr(' '.join(data[2:-1]))
                
                        if type(userAnswer) == "hello":
                            reportFormatError("{} :  Can't convert {} to (Complex) number ({})".format(data[0],' '.join(data[2:-1]), userAnswer))
                            perfect = False
                            judged.add(data[0])
                            continue

                        if len(data[-1]) == 2:
                            if not (data[-1][0] in "EPTGMkmunpfa"):
                                reportFormatError("{} : Wronf prefix unit ({}).".format(data[0], data[-1]))
                                perfect = False
                                judged.add(data[0])
                                continue
                            if data[-1][0] == 'E':
                                userAnswer *= 1e18
                            elif data[-1][0] == 'P':
                                userAnswer *= 1e15
                            elif data[-1][0] == 'T':
                                userAnswer *= 1e12
                            elif data[-1][0] == 'G':
                                userAnswer *= 1e9
                            elif data[-1][0] == 'M':
                                userAnswer *= 1e6
                            elif data[-1][0] == 'k':
                                userAnswer *= 1e3
                            elif data[-1][0] == 'm':
                                userAnswer *= 1e-3
                            elif data[-1][0] == 'u':
                                userAnswer *= 1e-6
                            elif data[-1][0] == 'n':
                                userAnswer *= 1e-9
                            elif data[-1][0] == 'p':
                                userAnswer *= 1e-12
                            elif data[-1][0] == 'f':
                                userAnswer *= 1e-15
                            elif data[-1][0] == 'a':
                                userAnswer *= 1e-18
                        
                        if VariableStuff.compareVar(userAnswer , ANS[data[0]][0], tol):
                            judged.add(data[0])
                            continue
                        else:
                            perfect = False
                            reportWrongAnswer("{} : Wrong Answer (Expected {} but got {})".format(data[0], userAnswer , ANS[data[0]][0]))
                            judged.add(data[0])
                            continue
                            
                    else:
                        reportFormatError("{} : Expect Equation but got Number".format(data[0], data[2]))
                        perfect = False
                        judged.add(data[0])
                        continue
                elif data[1] == ':':
                    if type(ANS[data[0]]) == type("hello"):

                        result = EquationStuff.convertAndCheck(" ".join(data[2:]))
                        if type(result) == type(""):
                            reportFormatError("{} Equation Error : {}".format(data[0], result))
                            perfect = False
                            judged.add(data[0])
                            continue
                        else:
                            if EquationStuff.compareEqual(" ".join(data[2:]),ANS[data[0]]):
                                judged.add(data[0])
                                continue
                            else:
                                reportWrongAnswer("{} : Wrong Answer (Here is example correct equation : {})".format(data[0], ANS[data[0]]))
                                perfect = False
                                judged.add(data[0])
                                continue
                    else:
                        reportFormatError("{} : Expect Number but got Equation".format(data[0], data[2]))
                        perfect = False
                        judged.add(data[0])
                        continue
        
        miss = "missing : "
        for k in ANS:
            if k not in judged:
                perfect = False
                miss += k + ", "
        
        if miss != "missing : ":
            reportFormatError(miss[:-2])
        
        if perfect:
            correct+=1
    
    return fullscore * correct / useLine
                            

if __name__ == '__main__':

    print("---NumberTest---")

    ref = 'V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A'
    outs = []
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = -24.51 V; I1 = 0.031 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = - 24.51 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = -0.149 A')
    outs.append('V1 = 24 V; I1 = 0.031 A\nV2 = 36.9 V; I2 = - 0.149 A')
    outs.append('V1 = 24 V; I1 = 0.03 A\nV2 = 37 V; I2 = -0.149 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = - 0.150 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = -0.150 A')
    outs.append('V1 = 24.5 V; I1 = 0.032 A\nV2 = 36.8 V; I2 = 0.150 A')


    for i, o in enumerate(outs):
        s1 = grading(o, ref, 10, "Test", "0.05")
        print('----')
        s2 = grading(o, ref, 10, "HidNum", "0.05")

        print("result:")
        print(o)
        print(i, ': numtol2(none)={}, (hidnum)={}'.format(s1, s2))
        print("end of test")
        print()

    print("\n\n---EquationTest---")

    ref = 'E1 : x + 2 x = 3;E2 : x + 3 = 0'
    outs = []
    outs.append('E1 : 3 x = 3;E2 : x = -3')
    outs.append('E1 : 3 x = 3;E2 : x = - 3')
    outs.append('E1 : 3 x - 3 = 0;E2 : x = - 3')
    outs.append('E1 : 3 x - 3 = 0;E2 : x + 3 = 0')
    outs.append('E1 : 3 y - 3 = 0;E2 : x + 3 = 0')
    outs.append('E1 : 3 y - 3 = 0;E2 : x = 3')
    outs.append('E1 : 3x = 3;E2 : x = -3')

    print('\n\n')
    for i, o in enumerate(outs):
        s1 = grading(o, ref, 10, "Test", "0.05")
        print('----')
        s2 = grading(o, ref, 10, "HidNum", "0.05")

        print("result:")
        print(o)
        print(i, ': numtol2(none)={}, (hidnum)={}'.format(s1, s2))
        print("end of test")
        print()

    print("\n\n---ComplexTest---")

    ref = 'C1 = 1 + 3i V'
    outs = []
    outs.append('C1 = 1 + 3i V')
    outs.append('C1 = 1+3i V')
    outs.append('C1 = complex(1,3) V')
    outs.append('C1 = -1 - 3i V')
    outs.append('C1 : 1-3i V')
    outs.append('E1 : 1+3i V')
    for i, o in enumerate(outs):
        s1 = grading(o, ref, 10, "Test", "0.05")
        print('----')
        s2 = grading(o, ref, 10, "HidNum", "0.05")

        print("result:")
        print(o)
        print(i, ': numtol2(none)={}, (hidnum)={}'.format(s1, s2))
        print("end of test")
        print()
    

    print("\n\nAutoLab Test")
    ref = """
Q1.1: V1 = 5 V; V2 = 0 V; I1 = -0.05 A; I2 = 0.05 A
Q1.2: V1 = 0 V; V2 = 8 V; I1 = 0 A; I2 = 0 A
Q1.3: V1 = 2.4 V; V2 = 0 V; I1 = -0.02 A; I2 = 0.02 A
Q1.4: V1 = 0 V; V2 = 0 V; I1 = -0.045 A; I2 = 0 A
Q1.5: V1 = 5 V; V2 = 5 V; I1 = -0.025 A; I2 = 0.025 A
"""

    me = """
Q1.1: V1 = 5 V; V2 = 0 V; I1 = -0.05 A; I2 = 0.05 A
Q1.2: V1 = 5 V; V2 = 0 V; I1 = -0.05 A; I2 = 0.05 A
Q1.3: V1 = 2.4 V; V2 = 0 V; I1 = -0.02 A; I2 = 0.02 A
Q1.4: V1 = 0 V; V2 = 0 V; I1 = -0.045 A; I2 = 0 A
Q1.5: V1 = 5 V; V2 = 5 V; I1 = -0.025 A; I2 = 0.025 A
"""
    s1 = grading(me, ref, 60, "Test", "0.05")
    print("Grading result :", s1, "of 60")


    s1 = grading("V1 = 1000 + 3000i V", "V1 = 1 + 3i kV", 60, "Test", "0.05")
    print("Grading result :", s1, "of 60")
    