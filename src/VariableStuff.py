
import math

class ComplexNumber:

    real = 0
    imagine = 0

    def __init__(self, real = 0, imagine = 0):
        self.real = real
        self.imagine = imagine
    
    #Convert any type to ComplexNumber
    def fromAny(any):
        if type(any) == type("hello"):
            return ComplexNumber.fromStr(any)
        elif type(any) == type(ComplexNumber(1,2)):
            return any
        elif type(any) == type(int()):
            return ComplexNumber(float(any),0)
        elif type(any) == type(float()):
            return ComplexNumber(any,0)
        elif type(any) == type(complex(1,3)):
            return ComplexNumber(any.real,any.imag)
        else:
            return "Type error ({})".format(type(any))

    def fromStr(content:str):

        re = 0.0
        im = 0.0


        # 3cis(0) is 3
        # -12cis(90) is -12i
        #AKA. Polar form
        if 'cis' in content:
            fac = 1
            spl = content.strip().replace("*",'').split('cis')
            if len(spl) > 2:
                return "too many 'cis' in  {}".format(content)
            
            if spl[0].strip():
                onlyNum = spl[0].strip()
                    
                try:
                    float(onlyNum)
                except:
                    return "Can't convert {} to number".format(onlyNum)

                fac *= float(onlyNum)

            

            spl2 = spl[1].strip().replace("(",'').split(')')
            if len(spl) > 2:
                return "too many ')' in  {}".format(content)

            onlyNum = spl2[0].strip()
            
            #Ang in dregree

            try:
                float(onlyNum)
            except:
                return "Can't convert {} to degree".format(onlyNum)
            
            im = math.sin(float(onlyNum))
            re = math.cos(float(onlyNum))

            if len(spl2) >= 2 and spl2[1].strip():
                onlyNum = spl2[1].strip()
                    
                try:
                    float(onlyNum)
                except:
                    return "Can't convert {} to number".format(onlyNum)

                fac *= float(onlyNum)
            im *= fac
            re *= fac
        # complex(1,3) is 1 + 3i
        elif 'complex' in content.lower():
            getter = content.lower().strip().split("complex")[1]
            getter = getter.replace('(','').split(')')[0]
            spl = getter.split(',')

            if len(spl) != 2:
                return "Wrong complex format in {}".format(content)
            
            for i,num in enumerate(spl):
                onlyNum = num.strip()
                
                try:
                    float(onlyNum)
                except:
                    return "Can't convert {} to number".format(num)
                
                if i == 0:re = float(onlyNum)
                else:im = float(onlyNum)
        #General Complex number format
        #EG. 12 + 3i
        else:
            spl = content.strip().split('+')
            for num in spl:
                if num.strip() == '':
                    continue

                splm = num.strip().split('-')
                for i,numm in enumerate(splm):
                    if numm.strip() == '':
                        continue
                        
                    
                    
                    if 'i' in numm or 'j' in numm:
                        onlyNum = numm.strip().replace('i','').replace('j','')
                        
                        try:
                            float(onlyNum)
                        except:
                            return "Can't convert {} to number".format(onlyNum)
                        
                        if i == 0:im += float(onlyNum)
                        else :im -= float(onlyNum)
                    else:
                        onlyNum = numm.strip().replace('i','').replace('j','')
                        try:
                            float(onlyNum)
                        except:
                            return "Can't convert {} to number".format(onlyNum)
                        
                        if i == 0:re += float(onlyNum)
                        else :re -= float(onlyNum)
        
        return ComplexNumber(re,im)
    
    def __mul__(self, other):
        re = self.real * other
        im = self.imagine  * other
        return ComplexNumber(re,im)
    

    def __str__(self) -> str:
        strResult = "{} ".format(self.real)

        if self.imagine != 0.0:
            if self.imagine > 0:
                strResult += "+ {}i ".format(self.imagine)
            else:
                strResult += "- {}i ".format(abs(self.imagine))

        return strResult

def compareVar(v1, v2, tol : float):
    c1 = ComplexNumber.fromAny(v1)
    c2 = ComplexNumber.fromAny(v2)
    
    if type(c1) == type('Hello'):
        return "Var 1 error : {}".format(c1)

    if type(c2) == type('Hello'):
        return "Var 2 error : {}".format(c2)
    
    delta = abs(c1.real - c2.real)
    delta += abs(c1.imagine - c2.imagine)

    return delta < tol
    



if __name__ == '__main__':

    print(ComplexNumber(1,3))
    print(ComplexNumber(1,-3))
    print(ComplexNumber(1,0))
    print(ComplexNumber(0,7))

    print(ComplexNumber.fromStr("1"))
    print(ComplexNumber.fromStr("-12"))
    print(ComplexNumber.fromStr("45.3"))
    print(ComplexNumber.fromStr("-87.1"))

    print(ComplexNumber.fromStr("3i"))
    print(ComplexNumber.fromStr("5i"))
    print(ComplexNumber.fromStr("-2i"))
    print(ComplexNumber.fromStr("-7.9i"))

    print(ComplexNumber.fromStr("1.45 + 3i"))
    print(ComplexNumber.fromStr("1.45+ 3i"))
    print(ComplexNumber.fromStr("1.45 +3i"))
    print(ComplexNumber.fromStr("1.45+3i"))
    print(ComplexNumber.fromStr("1.45 + 3 i"))
    print(ComplexNumber.fromStr("1.45+ 3 i"))
    print(ComplexNumber.fromStr("1.45 +3 i"))
    print(ComplexNumber.fromStr("1.45+3 i"))

    print(ComplexNumber.fromStr("1.45 - 3i"))
    print(ComplexNumber.fromStr("1.45- 3i"))
    print(ComplexNumber.fromStr("1.45 -3i"))
    print(ComplexNumber.fromStr("1.45-3i"))
    print(ComplexNumber.fromStr("1.45 - 3 i"))
    print(ComplexNumber.fromStr("1.45- 3 i"))
    print(ComplexNumber.fromStr("1.45 -3 i"))
    print(ComplexNumber.fromStr("1.45-3 i"))

    print(ComplexNumber.fromStr("- 1.45 - 3i"))
    print(ComplexNumber.fromStr("- 1.45- 3i"))
    print(ComplexNumber.fromStr("- 1.45 -3i"))
    print(ComplexNumber.fromStr("- 1.45-3i"))
    print(ComplexNumber.fromStr("- 1.45 - 3 i"))
    print(ComplexNumber.fromStr("- 1.45- 3 i"))
    print(ComplexNumber.fromStr("- 1.45 -3 i"))
    print(ComplexNumber.fromStr("- 1.45-3 i"))

    print(ComplexNumber.fromStr("- 1.45 + 3i"))
    print(ComplexNumber.fromStr("- 1.45+ 3i"))
    print(ComplexNumber.fromStr("- 1.45 +3i"))
    print(ComplexNumber.fromStr("- 1.45+3i"))
    print(ComplexNumber.fromStr("- 1.45 + 3 i"))
    print(ComplexNumber.fromStr("- 1.45+ 3 i"))
    print(ComplexNumber.fromStr("- 1.45 +3 i"))
    print(ComplexNumber.fromStr("- 1.45+3 i"))

    print(ComplexNumber.fromStr("- 1.45+3i - 1.45"))


    print(ComplexNumber.fromStr("7 cis(45)"))
    print(ComplexNumber.fromStr("7cis(45)"))
    print(ComplexNumber.fromStr("3.5cis(45)2"))

    for i in range(0,360,30):
        print(ComplexNumber.fromStr("10cis({})".format(i)))
    
    print(ComplexNumber.fromStr("complex(1,2)"))
    print(ComplexNumber.fromStr("complex(1,-2)"))
    print(ComplexNumber.fromStr("complex(-1,-2)"))
    print(ComplexNumber.fromStr("complex(-1,2)"))
    print(ComplexNumber.fromStr("complex( -1  , 2 )"))
    print(ComplexNumber.fromStr("Complex(-1,2)"))
    print(ComplexNumber.fromStr("CoMpLeX(-1,2)"))


    print(compareVar("3 + 4i", "4i + 3",0.05))
    print(compareVar("3 + 4i", "complex(3,4)",0.05))
    print(compareVar("3 + 4i", "1 + 2 + 4i",0.05))
    print(compareVar("3 + 4i", "3 + 4j",0.05))

    print(compareVar(ComplexNumber(3,4), "3 + 4j",0.05))
    print(compareVar(ComplexNumber(3,4), "3 + 1j",0.05))
    print(compareVar(ComplexNumber(3,1), "3 + 1j",0.05))
    print(compareVar(12.3, "3 + 1j",0.05))
    print(compareVar(7, complex(7,0),0.05))
    print(compareVar(7, complex(7),0.05))

    print(ComplexNumber.fromStr("3+1j"))
    print(ComplexNumber.fromStr("2i-1"))
    print(ComplexNumber.fromStr("."))
    

