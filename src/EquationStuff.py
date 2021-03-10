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
            if vars[i][0] == key:
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
        if self.num != 0.0:strRes += f"{self.num} "
        
        for var in self.vars:

            if var[1] == 1:
                strRes += f"+ "
            elif var[1] > 1:
                strRes += f"+ {var[1]}"
            elif var[1] == -1:
                strRes += f"- "
            elif var[1] < -1:
                strRes += f"- {abs(var[1])}"
            else:continue


            for v in var[0]:
                if v[1] == 0:
                    continue
                elif v[1] == 1:
                    strRes += f"{v[0]}"
                elif v[1] > 1:
                    strRes += f"{v[0]}^{v[1]}"
                else:
                    strRes += f"{v[0]}^({v[1]})"

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

    return stackNumber[-1];

def convertAndCheck(equ:str):
    content = equ.strip().split('=')
    
    equations = []
    if len(content) > 2:
        return "too much '='"
    for equa in content:
        con = str2CppCmp(equa.strip())
        paren = 0
        for e in con:
            if e == '(':
                paren += 1
            elif e == ')':
                paren -= 1
            if paren < 0:
                return "Parentheses Error"
        
        if paren != 0:
            return "Parentheses Error"
        
        result = [con[0]]
        pre = con[0]

        for i in range(1,len(con)):
            if pre not in "+-*/()" and con[i] not in "+-*/()":
                result.append("*")
            elif pre not in "+-*/()" and con[i] in "(":
                result.append("*")
            elif pre in ")" and con[i] not in "+-*/()":
                result.append("*")
            result.append(con[i])
            pre = con[i]
        equations.append(result)


        lastEquations = []

        for equ in equations:
            thisEqu = []
            for e in equ:
                
                
                num = ""
                var = ""
                isNumBruh = True 

                for c in e:
                    if isNumBruh and (c.isnumeric() or c == '.' or c == '-'):
                        num += c
                    else:
                        var += c
                        isNumBruh = False
                
                if num.strip() == '' and var.strip() == '':
                    continue

                if num.strip() == '':
                    thisEqu.append(var.strip())
                    continue

                if num == '-':
                    thisEqu.append(e)
                    continue

                try:
                    float(num)
                except:
                    return "NumError : {}".format(num)
                    
                if len(num) > 0 and len(var) > 0:
                    thisEqu.append(num)
                    thisEqu.append("*")
                    thisEqu.append(var)
                else:
                    thisEqu.append(e)
            lastEquations.append(thisEqu)

    

    return lastEquations

def compareEqual(equ1:str, equ2:str):
    resultE1 = convertAndCheck(equ1)
    if type(resultE1) == type(str()):
        return f"Equ 1 error : {resultE1}"
    
    resultE2 = convertAndCheck(equ2)
    if type(resultE2) == type(str()):
        return f"Equ 2 error : {resultE2}"


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
                if (G_Fac - var[1] / solution2.vars[res][1]) / G_Fac >= 0.01:
                    return False
        else:
            return False
     
    return True


if __name__ == "__main__" :
    

    print(compareEqual("4","4"))
    print(compareEqual("4 + 2","6"))
    print(compareEqual("0 = 2 x + 3 y ","2 x + 3 y = 0"))
    print(compareEqual("-  2 x = + 3 y ","2 x + 3 y = 0"))
    print(compareEqual("- 2 x - 3 y = 0","2 x + 3 y = 0"))
    print(compareEqual("- 2 x - 3 y + 1 = 1","2 x + 3 y = 0"))
    print(compareEqual("2 x + 3 y = 0","2 x + 3 y = 0"))

    print("WA")
    print(compareEqual("2 x + 3 y ","- 2 x + 3 y"))

    print("\nTest")
    print(compareEqual("Vy + Vx = - 2 * Vx + 5","Vx + Vy + 2 * Vx = 5"))

    print(compareEqual("Vx * Vx + Vy = 2", "Vx * Vx = 2 - Vy"))
    print(compareEqual("3 Vx = 3","Vx = 1"))
    print(compareEqual("3Vx = 3","1 = Vx"))
    print(compareEqual("3Vx = 3","1 + Vx"))
    print(compareEqual("3y * i + ( 3x - 6y ) * j","3y * (i + j) + ( x - y ) * 3j"))