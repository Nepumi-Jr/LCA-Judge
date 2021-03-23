#from LCA_Judge.src 
from LCA_Judge.src import EquationStuff
from LCA_Judge.src import VariableStuff
from LCA_Judge.src import BigAnswerConvert

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
        #Convert chunk to data by BigAnswerConvert
        data = BigAnswerConvert.bigConvert(chunk.strip())

        if type(data) == type("Error"):
            print("refAns Error {}".format(data))
            continue
            
        ANS[data[1]] = data
            
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
            data = BigAnswerConvert.bigConvert(chunk.strip())

            if data[1] in ANS and data[1] not in judged:

                if data[0] != ANS[data[1]][0]:
                    reportFormatError("{} : Expected {} but got {}".format(data[1], ANS[data[1]][0]=='E' and 'Equation' or 'Number', data[0]=='E' and 'Equation' or 'Number'))
                    perfect = False
                    judged.add(data[0])
                    continue

                if data[0] == 'E':
                    if EquationStuff.compareEqual(data[2], ANS[data[1]][2]):
                        judged.add(data[1])
                        continue
                    else:
                        perfect = False
                        reportWrongAnswer("{} : Wrong Answer (Here is an Example {})".format(data[1], ANS[data[1]][2]))
                        judged.add(data[1])
                        continue
                else:
                    if data[3] != ANS[data[1]][3]:
                        perfect = False
                        reportWrongAnswer("{} : Wrong Answer (Expected {} but got {})".format(data[1], str(data[2]) + data[3] , str(ANS[data[1]][2]) + ANS[data[1]][3]))
                        judged.add(data[1])
                        continue
                    elif VariableStuff.compareVar(data[2], ANS[data[1]][2], tol):
                        judged.add(data[1])
                        continue
                    else:
                        perfect = False
                        reportWrongAnswer("{} : Wrong Answer (Expected {} but got {})".format(data[1], str(data[2]) + data[3] , str(ANS[data[1]][2]) + ANS[data[1]][3]))
                        judged.add(data[1])
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
    