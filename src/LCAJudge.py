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
import BigAnswerConvert

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

def DEBUG(x):
    if testCase != "2":
        print(f"D;0;1;0;0;{x}")
    else:
        print(f"E;0;1;0;0;ENDED")

def getNumTol():

    DEF_TOL = 0.001

    if path.exists(path.join(PROBLEM_DIR,"numtol.txt")):
        try:
            with open(path.join(PROBLEM_DIR,"numtol.txt"),"r") as f:
                DEBUG(f.read().strip())
                float(f.read().strip())
                return abs(float(f.read().strip()))
        except:
            return DEF_TOL
    
    return DEF_TOL


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

        data = BigAnswerConvert.bigConvert(line.strip())
        if type(data) != type("Hello"):
            ANS.append(data)

    MAX_TEST = len(ANS)

def variableCompare(data):
    tc = int(testCase) - 1 
    tol = getNumTol()

    if VariableStuff.compareVar(data[2] , ANS[tc][2], tol) and data[3].lower() == ANS[tc][3].lower():
        return "P",1,1,"Wow za!"
    else:
        return "-",0,1,f"{data[1]} : Wrong Answer"

def equationCompare(data):
    tol = getNumTol()
    if EquationStuff.compareEqual(data[2],ANS[int(testCase) - 1][2],tol):
        return "P",1,1,"Complete"
    else:
        return "-",0,1,f"{data[1]} : Wrong answer"
            

def compare():

    userStr = ""
    try:
        with open(srcPath,"r") as f:
            userStr = f.read().strip().replace("\r","").split("\n")
    except:
        return "!",0,1,"Answer not found :("

    tc = int(testCase) - 1    

    for line in userStr:
        data = BigAnswerConvert.bigConvert(line.strip())
        tc = int(testCase) - 1 

        if type(data) == type("Hello"):
            continue

        if data[1] == ANS[tc][1]:

            if ANS[tc][0] != data[0]:
                return "X",0,1,f"{ANS[tc][1]} : Expected {ANS[tc][0] == 'E' and 'Equation' or 'Number'} got {data[0] == 'E' and 'Equation' or 'Number'}"

            if data[0] == 'V':
                return variableCompare(data)
            elif data[0] == "E":
                return equationCompare(data)

    return "X",0,1,f"{ANS[tc][1]} not found or Wrong format... :("

    


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
