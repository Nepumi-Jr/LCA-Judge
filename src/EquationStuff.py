#Do hard work with Meow :3

from copy import deepcopy
def precedence(symbol:str) -> int:
    if symbol == '+' or symbol == '-':
        return 1
    elif symbol == '*' or symbol == '/':
        return 2
    else:
        return -1

def str2CppCmp(x:str) -> list():
    res = []
    x = x.replace("\r","").split("\n")
    for e in x:
        for f in e.strip().split(" "):
            if f.strip():
                res.append(f.strip())
    
    return res

def findLast(content:str,sym:str) -> int:
    for i in range(len(content) - 1,-1,-1):
        if content[i] == sym:
            return i
    return -1

def compareVarAdv(l1:list,l2:list) -> bool:
    l1s = set()
    l2s = set()
    for v1 in l1:
        if v1[0].find("(") != -1:
            l1s.add((v1[0][:v1[0].find("(")],v1[1]))
        else:
            l1s.add((v1[0],v1[1]))
    
    for v2 in l2:
        if v2[0].find("(") != -1:
            l2s.add((v2[0][:v2[0].find("(")],v2[1]))
        else:
            l2s.add((v2[0],v2[1]))
    
    return l1s == l2s

class Pod(object):
    
    num = 0
    vars = []
    
    def __init__(self, num:float, vars:list) -> None:
        self.num = num
        self.vars = vars

    def copy(self):
        return Pod(self.num,deepcopy(self.vars))
    

    def findVarInd(self, vars, key):
        for i in range(len(vars)):
            if compareVarAdv(vars[i][0],key):
                return i
        return -1
    

    def doSort(self):
        for i in range(len(self.vars)):
            self.vars[i][0] = sorted(self.vars[i][0],key = lambda x: x[0])
    
    def doVerify(self):
        newVars = []
        for v in self.vars:
            if v[1] != 0:
                newV = []
                for subV in v[0]:
                    if subV[1] != 0:
                        newV.append(subV)
                    
                if len(newV) == 0:
                    self.num += v[1]
                else:
                    newVars.append([newV,v[1]])
        
        self.vars = newVars

    def __add__(self, other):
        self.doSort()
        other.doSort()
        numRes = self.num + other.num
        varsRes = deepcopy(self.vars)

        for var in other.vars:
            if self.findVarInd(varsRes, var[0]) == -1:
                varsRes.append(var)
            else:
                varsRes[self.findVarInd(varsRes, var[0])][1] += var[1]
        
        return Pod(numRes, varsRes)

    def __sub__(self, other):

        self.doSort()
        other.doSort()
        numRes = self.num - other.num
        varsRes = deepcopy(self.vars)

        for var in other.vars:
            if self.findVarInd(varsRes, var[0]) == -1:
                varsRes.append([var[0],-var[1]])
            else:
                varsRes[self.findVarInd(varsRes, var[0])][1] -= var[1]
        
        return Pod(numRes, varsRes)
    
    def __mul__(self, other):
        self.doSort()
        other.doSort()
        res = Pod(0.0,[])

        num1 = self.copy()
        num2 = other.copy()

        res.num = num1.num * num2.num
        #num * all
        for v in num1.vars:
            temp = [deepcopy(v)]
            temp[0][1] *= num2.num
            res += Pod(0.0, temp)
        
        #all * num
        for v in num2.vars:
            temp = [deepcopy(v)]
            temp[0][1] *= num1.num
            res += Pod(0.0, temp)

        #all * all
        for v1 in num1.vars:
            for v2 in num2.vars:
                newVar = []
                comVar = set()
                
                for mv1 in v1[0]:
                    founded = False
                    for mv2 in v2[0]:
                        if mv1[0] == mv2[0]:
                            newVar.append([mv1[0],mv1[1] + mv2[1]])
                            comVar.add(mv1[0])
                            founded = True
                            break
                            
                    if not founded:
                        comVar.add(mv1[0])
                        newVar.append(mv1)
                
                for mv2 in v2[0]:
                    if not mv2[0] in comVar:
                        comVar.add(mv2[0])
                        newVar.append(mv2)
                
                    
                temp = [[newVar ,v1[1] * v2[1]]]
                res += Pod(0.0,temp)
        return res
    
    def __truediv__(self, other):
        self.doSort()
        other.doSort()
        res = Pod(0.0,[])

        num1 = self.copy()
        num2 = other.copy()

        def fastDiv(n1:float,n2:float):
            if n1 == 0.0 or n2 == 0.0:
                return 0
            else:
                return n1/n2 

        res.num = fastDiv(num1.num , num2.num)
        #num * all
        for v in num1.vars:
            temp = [v.copy()]
            temp[0][1] = fastDiv(temp[0][1] , num2.num)
            res += Pod(0.0,temp)
        
        #all * num
        for v in num2.vars:
            temp = [v.copy()]
            temp[0][1] = fastDiv(temp[0][1] , num1.num)
            res += Pod(0.0,temp)

        #all * all
        for v1 in num1.vars:
            for v2 in num2.vars:
                newVar = []
                comVar = set()
                
                for mv1 in v1[0]:
                    founded = False
                    for mv2 in v2[0]:
                        if mv1[0] == mv2[0]:
                            newVar.append([mv1[0],mv1[1] - mv2[1]])
                            comVar.add(mv1[0])
                            founded = True
                            break
                            
                    if not founded:
                        comVar.add(mv1[0])
                        newVar.append(mv1)
                
                for mv2 in v2[0]:
                    if not mv2[0] in comVar:
                        comVar.add(mv2[0])
                        newVar.append(mv2)
                
                    
                temp = [[newVar ,fastDiv(v1[1] , v2[1])]]
                res = doOperator(res,"+",Pod(0.0,temp))
        res.doVerify()
        return res

    def __str__(self):
        strRes = ""
        if self.num != 0.0:strRes += "{} ".format(self.num)
        
        for var in self.vars:

            if var[1] == 1:
                strRes += "+ "
            elif var[1] > 1:
                strRes += "+ {}".format(var[1])
            elif var[1] == -1:
                strRes += "- "
            elif var[1] < -1:
                strRes += "- {}".format(abs(var[1]))
            else:continue


            for v in var[0]:
                if v[1] == 0:
                    continue
                elif v[1] == 1:
                    strRes += "{}".format(v[0])
                elif v[1] > 1:
                    strRes += "{}^{}".format(v[0],v[1])
                else:
                    strRes += "{}^({})".format(v[0],v[1])

            strRes += ' '

        return strRes.strip() 
        #f'\nRaw data : [{self.num}] [{self.vars}]'



def doOperator(n1:Pod,opera:str,n2:Pod) -> float:

    if opera == '+':
        return n1 + n2
    elif opera == '-':
        return n1 - n2
    elif opera == '*':
        return n1 * n2
    elif opera == '/':
        return n1 * n2

def isSymbol(ss:str) -> bool:
    return (ss in "+-*/()")

def isNum(ss:str) -> bool:
    if ss == ".":return True
    try:
        float(ss)
        return True
    except:
        return False




def solveInfix(equ:list) -> Pod:

    #Infix to Postfix

    posfix = []
    stackOperator = []

    for nos in equ:#nos is num or symbol
        if not isSymbol(nos):

            if isNum(nos):
                posfix.append(Pod(float(nos), []))
            else:
                posfix.append(Pod(0.0,[[[[nos,1]],1]]))

        else:
            if nos != "(" and nos != ")":
                while len(stackOperator) > 0 and stackOperator[-1] != "(" \
                and precedence(nos) <= precedence(stackOperator[-1]):
                    posfix.append(stackOperator.pop())
                stackOperator.append(nos)
            else:
                if nos == "(":
                    stackOperator.append(nos)
                else:
                    while len(stackOperator) > 0 and stackOperator[-1] != "(" :
                        posfix.append(stackOperator.pop())
                    stackOperator.pop()
    
    while len(stackOperator) > 0:
        posfix.append(stackOperator.pop())
    


    #Postfix to answer
    stackNumber = [Pod(0.0,[]), Pod(0.0,[])]
    for pos in posfix:
        if type(pos) == type(Pod(0.0,[])):
            stackNumber.append(pos)
        else:
            n1 = stackNumber.pop()
            n2 = stackNumber.pop()
            stackNumber.append(doOperator(n2,pos,n1))

    return stackNumber[-1]

def convertAndCheck(equ:str):
    content = equ.strip().replace(" ","").split('=')
    
    equations = []
    if len(content) > 2:
        return "too much '='"
    
    if len(content) == 1:
        return "No '=' in equation."

    for equa in content:
        thisEqu = []
        hold = ""
        mode = "?" #N V or ?
        tempP = 0
        

        for sym in equa:
            if mode == "N":
                if isNum(hold + sym):
                    hold += sym
                elif sym in "+-*/()":
                    thisEqu.append(hold)
                    thisEqu.append(sym)
                    hold = ""
                    mode = "?"
                else:
                    thisEqu.append(hold)
                    hold = sym
                    mode = "V"
                    firstPar = True
            elif mode == "V":
                if sym in "+-*/":
                    if tempP > 0:
                        hold += sym
                    else:
                        thisEqu.append(hold)
                        thisEqu.append(sym)
                        hold = ""
                        mode = "?"
                elif sym == "(":
                    tempP += 1
                    hold += sym
                elif sym == ")":
                    tempP -= 1
                    if tempP == 0:
                        thisEqu.append(hold+sym)
                        hold = ""
                        mode = "?"
                    else:
                        hold += sym
                    
                else:
                    hold += sym
            else:
                if isNum(sym):
                    hold = sym
                    mode = "N"
                elif sym in "+-*/()":
                    thisEqu.append(sym)
                else:
                    firstPar = True
                    mode = "V"
                    hold = sym
        
        if (mode == "N" or mode == "V") and hold != '':
            thisEqu.append(hold)
        

        realThisEqu = []
        realThisEqu.append(thisEqu[0])

        for i in range(1,len(thisEqu)):
            stuff = thisEqu[i];

            if realThisEqu[-1] not in "+-*/()" and stuff not in "+-*/()":
                realThisEqu.append("*")
            elif realThisEqu[-1].endswith(")") and stuff.startswith("("):
                realThisEqu.append("*")
            elif realThisEqu[-1].endswith(")") and stuff not in "+-*/()":
                realThisEqu.append("*")
            realThisEqu.append(stuff)

        equations.append(realThisEqu)



    return equations

def compareEqual(equ1:str, equ2:str):
    resultE1 = convertAndCheck(equ1)
    if type(resultE1) == type(str()):
        return "Equ 1 error : {}".format(resultE1)
    
    resultE2 = convertAndCheck(equ2)
    if type(resultE2) == type(str()):
        return "Equ 2 error : {}".format(resultE2)


    solution1 = solveInfix(resultE1[0])
    for i in range(1,len(resultE1)):
        solution1 -= solveInfix(resultE1[i])
    solution1.doVerify()

    solution2 = solveInfix(resultE2[0])
    for i in range(1,len(resultE2)):
        solution2 -= solveInfix(resultE2[i])
    solution2.doVerify()

    G_Fac = 1.0
    G_Done = False
    
    
    if solution1.num == 0 or solution2.num == 0:
        if solution1.num != 0 or solution2.num != 0:
            return False
    else:
        G_Fac = solution1.num / solution2.num
        G_Done = True
    
    
    if len(solution1.vars) != len(solution2.vars):
        return False
    
    for var in solution1.vars:
        res = solution2.findVarInd(solution2.vars,var[0])
        if res != -1:
            if not G_Done:
                G_Fac = var[1] / solution2.vars[res][1]
                G_Done = True
            else:
                if abs(G_Fac - var[1] / solution2.vars[res][1]) / G_Fac >= 0.01:
                    return False    
            
            #Compare function
            for miniV in var[0]:
                if miniV[0].find("(") != - 1:
                    findV2 = -1
                    for miniV2 in solution2.vars[res][0]:
                        if miniV2[0].find("(") != - 1:
                            if miniV2[0][:miniV2[0].find("(")] == miniV[0][:miniV[0].find("(")]:
                                findV2 = miniV2[0]
                    
                    if findV2 == -1:
                        return False
                    findV1 = miniV[0]
                    
                    newE1 = findV1[findV1.find("(") + 1 : findLast(findV1,")")]+"=0"
                    newE2 = findV2[findV2.find("(") + 1 : findLast(findV2,")")]+"=0"

                    if compareEqual(newE1,newE2) == False:
                        return False


            
        else:
            return False
    
    
    return True


if __name__ == "__main__" :
    
    # print(compareEqual("0 = 2 x + 3 y ","2 x + 3 y = 0"))
    # print(compareEqual("-  2 x = + 3 y ","2 x + 3 y = 0"))
    # print(compareEqual("- 2 x - 3 y = 0","2 x + 3 y = 0"))
    # print(compareEqual("- 2 x - 3 y + 1 = 1","2 x + 3 y = 0"))
    # print(compareEqual("2 x + 3 y = 0","2 x + 3 y = 0"))

    # print("WA")
    # print(compareEqual("2 x + 3 y = 0 ","- 2 x + 3 y = 0"))

    # print("\nTest")
    # print(compareEqual("Vy + Vx = - 2 * Vx + 5","Vx + Vy + 2 * Vx = 5"))

    # print(compareEqual("Vx * Vx + Vy = 2", "Vx * Vx = 2 - Vy"))
    # print(compareEqual("3 Vx = 3","Vx = 1"))
    # print(compareEqual("3Vx = 3","1 = Vx"))
    # print(compareEqual("3Vx = 3","-1 + Vx = 0"))
    # print(compareEqual("3y * i + ( 3x - 6y ) * j = 0","3y * (i + j) + ( x - y ) * 3j = 0"))

    # print(compareEqual("xy = 0","x * y = 0"))
    # print(compareEqual("x y = 0","x * y = 0"))
    # print(compareEqual("y * x = 0","x * y = 0"))

    # print(compareEqual("V(t) = t * t - 1 t - 12","V(t) = ( t - 4 ) * ( t + 3 )"))


    # print(compareEqual("V(T) = 1/12/35exp(x+2)", "V(T) = 1/(12*35)exp(x+1+1)"))
    print(convertAndCheck("Vc = 12 - 8 exp(-12.5 t) V"))
    print(convertAndCheck("Vx = func(12 + x)(y+3)"))
    print(compareEqual("Vc = 12 - 8 exp(-12.5 t) V","Vc = 12 - 8 exp(-12.5 t)"))