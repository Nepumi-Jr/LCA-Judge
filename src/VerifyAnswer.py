import sys
from os import path
import EquationStuff
import VariableStuff

if len(sys.argv) < 2:
    print("no input file :(",file=sys.stderr)
    exit(1)

fileVeri = sys.argv[-1]

if not path.exists(fileVeri):
    print("input file not found",file=sys.stderr)
    exit(1)

with open(fileVeri,"r") as f:
    content = f.read().strip().replace("\r","").split("\n")


def str2CppCmp(x:str) -> list():
    res = []
    x = x.replace("\r","").split("\n")
    for e in x:
        for f in e.strip().split(" "):
            if f.strip():
                res.append(f.strip())
    
    return res

ANS = []

for line in content:
    data = str2CppCmp(line.strip())
    if data[1] == '=':
        if len(data[-1]) > 2:
            print(f"Warning {data[0]} : Wrong Unit ({data[-1]})",file=sys.stderr)
            continue
        
        solAnswer = VariableStuff.ComplexNumber.fromStr(' '.join(data[2:-1]))
            
        if type(solAnswer) == type("hello"):
            print(f"Warning {data[0]} : Can't convert to number ({solAnswer})",file=sys.stderr)
            continue

        if len(data[-1]) == 2:
            if not (data[-1][0] in "EPTGMkmunpfa"):
                print(f"Warning {data[0]} : Wrong unit ({data[-1]})",file=sys.stderr)
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
        ANS.append((data[0],solAnswer,data[-1][-1]))
    elif data[1] == ':':

        ansRef = EquationStuff.convertAndCheck(" ".join(data[2:]))

        if type(ansRef) == type(str()):
            print(f"Warning {data[0]} : Equation Error ({ansRef})",file=sys.stderr)
            continue
        else:
            ANS.append((data[0],ansRef))


        



if len(ANS) == 0:
    print("\n--------------------------\nProblem Error : No correctly Answer\nAre you type the correct format?\n\nYou can read format in",file=sys.stderr)
    print(r"",file=sys.stderr)
    exit(1)

exit(0)







