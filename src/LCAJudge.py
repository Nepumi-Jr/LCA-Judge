"""
    Input by 9 or more argument
    1 : test case
    2 : timeLimit in ms
    3 : memoryLimit in mb
    4 : PROBLEM_DIR
    5 : source path
    6 : cmp cmd
    7 : cmp args
    8 : run cmd
    9 : run args

    output will return by stdout in formating below
    {verdic};{score};{maxscore};{elapsed};{memory};{comment}
"""



from os import path
import os
import sys
from subprocess import Popen,TimeoutExpired,PIPE
import time
import signal
import EquationStuff
import VariableStuff

judgeArgs = sys.argv[-1]

if not path.exists(judgeArgs):
    print(f"!;0;1;0;0;Judge args not found :(",end = "")
    exit(0)

try:
    with open(judgeArgs,"r") as f:
        judgeArgs = f.read().split("\n")

except:
    print(f"!;0;1;0;0;Can't read Judge args:(",end = "")
    exit(0)

if(len(judgeArgs) < 9):
    print(f"!;0;1;0;0;Not Enough info to judge\nexpected 9 args got {len(judgeArgs)} args",end = "")
    exit(0)

try:

    testCase = judgeArgs[0] or ""
    timeLimit = int(judgeArgs[1] or "")#In ms
    memoryLimit = int(judgeArgs[2] or "")#mb
    PROBLEM_DIR = judgeArgs[3] or ""
except:
    print(f"!;0;1;0;0;Can't convert data :(",end = "")
    exit(0)

if(len(judgeArgs) < 6):
    print(f"!;0;1;0;0;Program not Found",end = "")
    exit(0)


srcPath = judgeArgs[4] or ""

cmpMain = judgeArgs[5] or ""
cmpArg = judgeArgs[6] or ""

outMain = judgeArgs[7]
outArg = judgeArgs[8]


def writeLog(text:str):
    with open(path.join(PROBLEM_DIR,f"{int(time.time())}T{testCase}LOG.txt"),"w") as f:
        f.write(text)



def str2CppCmp(x:str) -> list():
    res = []
    x = x.replace("\r","").split("\n")
    for e in x:
        for f in e.strip().split(" "):
            if f.strip():
                res.append(f.strip())
    
    return res

ANS = []
MAX_TEST = len(ANS)

def readSolution():

    global ANS,MAX_TEST

    if not path.exists(path.join(PROBLEM_DIR,"answer.txt")):
        if testCase == "1":
            print(f"!;0;1;0;0;answer.txt not found",end = "")
            exit(0)
        else:
            print(f"E;0;0;0;0;End of Test",end = "")
            exit(0)
    with open(path.join(PROBLEM_DIR,"answer.txt"),"r") as f:
        content =  f.read().strip().replace("\r","").split("\n")
    
    

    for line in content:
        data = str2CppCmp(line.strip())

        if data[1] == '=':

            if len(data[-1]) > 2:
                continue

            solAnswer = VariableStuff.ComplexNumber.fromStr(' '.join(data[2:-1]))
            
            

            if type(solAnswer) == type("hello"):
                continue

            if len(data[-1]) == 2:
                if not (data[-1][0] in "EPTGMkmunpfa"):
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
        
            ANS.append((data[0],solAnswer,data[-1][-1]))
        else:
            if data[1] == ':' and type(EquationStuff.convertAndCheck(" ".join(data[2:]))) != type(str()) :
                ANS.append((data[0]," ".join(data[2:])))

    
    MAX_TEST = len(ANS)

def variableCompare(data):
    tc = int(testCase) - 1    
    if len(data[-1]) > 2:
        return "X",0,1,f"{data[0]} : Wrong Unit Format in {data[0]}"

    if data[-1][-1] != ANS[tc][2]:
        return "-",0,1,f"{data[0]} : Wrong Unit (Expect {ANS[tc][2]} but got {data[3][-1]})"

    userAnswer = VariableStuff.ComplexNumber.fromStr(' '.join(data[2:-1]))
        
    if type(userAnswer) == type("hello"):
        return "X",0,1,"refAns Error :in variable {} Can't convert {} to (Complex) number ({})".format(data[0],' '.join(data[2:-1]), userAnswer)

    if len(data[-1]) == 2:
        if not (data[-1][0] in "EPTGMkmunpfa"):
            return "-",0,1,f"{data[0]} : Wat format? {data[-1]}!?"
        
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


    if VariableStuff.compareVar(userAnswer , ANS[tc][1], 0.05):
        return "P",1,1,"Wow za!"
    else:
        return "-",0,1,f"{data[0]} : Wrong Answer"

def equationCompare(data):
    userRes = EquationStuff.convertAndCheck(" ".join(data[2:]))
    if type(userRes) == type(str()):
        return "X",0,1,f"{data[0]} Error : {userRes}"
    else:
        if EquationStuff.compareEqual(" ".join(data[2:]),ANS[int(testCase) - 1][1]):
            return "P",1,1,"Complete"
        else:
            return "-",0,1,f"{data[0]} : Wrong answer"
            

def compare():

    userStr = ""
    try:
        with open(srcPath,"r") as f:
            userStr = f.read().strip().replace("\r","").split("\n")
    except:
        return "!",0,1,"Answer not found :("

    tc = int(testCase) - 1    

    for line in userStr:
        data = str2CppCmp(line)
        
        tc = int(testCase) - 1 
        if data[0] == ANS[tc][0]:
            if ANS[tc][1] == ':' and data[1] == '=':
                return "X",0,1,f"{ANS[tc][0]} : Expected Equation got Number"
            if ANS[tc][1] == '=' and data[1] == ':':
                return "X",0,1,f"{ANS[tc][0]} : Expected Number got Equation"

            if data[1] == '=':
                return variableCompare(data)
            elif data[1] == ":":
                return equationCompare(data)

    return "X",0,1,f"{ANS[tc][0]} not found or Wrong format... :("

    


#This is from Kiyago's standard judge
def main():


    readSolution()

    if int(testCase) > MAX_TEST:
        print(f"E;0;0;0;0;End of Test",end = "")
        return

    verdic,score,maxscore,comment = compare()


    # Clean up tmp directory
    try:
        #if(path.exists(outPath)):os.remove(outPath)
        #if(path.exists(errPath)):os.remove(errPath)
        pass
    except:
        pass

    print(f"{verdic};{score};{maxscore};0;0;{comment}",end = "")

main()
