import sys
from os import path
import BigAnswerConvert

if len(sys.argv) < 2:
    print("no input file :(",file=sys.stderr)
    exit(1)

answerReporter = False

if len(sys.argv) == 2:
    fileVeri = sys.argv[-1]
elif len(sys.argv) == 3:
    fileVeri = sys.argv[1]
    answerReporter = True

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

    res = BigAnswerConvert.bigConvert(line.strip())
    if type(res) == type("Error"):
        print(res)
    else:
        ANS.append(res)



if len(ANS) == 0:
    print("\n--------------------------\nProblem Error : No correctly Answer\nAre you type the correct format?\n\nYou can read format in",file=sys.stderr)
    print(r"",file=sys.stderr)
    exit(1)

if answerReporter:
    print("===Here is answer that Accepted===")
    for ans in ANS:
        print(ans[0],"is",ans[1],end = " ")

        if len(ans) > 2 :
            print(ans[2])
        else:
            print()

exit(0)







