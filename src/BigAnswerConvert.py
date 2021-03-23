import VariableStuff
import EquationStuff

def bigConvert(someContent : str):
    if ":" not in someContent:
        nameVar = someContent.strip().replace(" ",'').split("=")[0]
        data = someContent.strip().replace(" ",'').split("=")[-1]

        if data[-2] in "EPTGMkmunpfa":
            solAnswer = VariableStuff.ComplexNumber.fromStr(data[:-2])
            if type(solAnswer) == type("hello"):
                return "Warning {} : {}".format(nameVar,solAnswer)

            if data[-2] == 'E':
                solAnswer *= 1e18
            elif data[-2] == 'P':
                solAnswer *= 1e15
            elif data[-2] == 'T':
                solAnswer *= 1e12
            elif data[-2] == 'G':
                solAnswer *= 1e9
            elif data[-2] == 'M':
                solAnswer *= 1e6
            elif data[-2] == 'k':
                solAnswer *= 1e3
            elif data[-2] == 'm':
                solAnswer *= 1e-3
            elif data[-2] == 'u':
                solAnswer *= 1e-6
            elif data[-2] == 'n':
                solAnswer *= 1e-9
            elif data[-2] == 'p':
                solAnswer *= 1e-12
            elif data[-2] == 'f':
                solAnswer *= 1e-15
            elif data[-2] == 'a':
                solAnswer *= 1e-18
            
            return ("V",nameVar,solAnswer,data[-1])
        else:
            solAnswer = VariableStuff.ComplexNumber.fromStr(data[:-1])
            if type(solAnswer) == type("hello"):
                return "Warning {} : {}".format(nameVar,solAnswer)
            return ("V",nameVar,solAnswer,data[-1])
    else:
        nameVar = someContent.strip().replace(" ",'').split(":")[0]
        data = someContent.strip().replace(" ",'').split(":")[-1]
        
        res = EquationStuff.convertAndCheck(data)
        if type(res) == type("hello"):
            return "Warning {} : {}".format(nameVar,res)

        return ("E",nameVar,data)




if __name__ == "__main__":

    def printWow(content):
        print("Type",content[0],content[1],"is",content[2],end = " ")

        if len(content) > 3 :
            print(content[3])
        else:
            print()


    printWow(bigConvert("I1 = 1.2 A"))
    printWow(bigConvert("I1=1.2A"))
    printWow(bigConvert("I1=       1.2mA"))
    printWow(bigConvert("I1 7 = 1.2A"))


    printWow(bigConvert("KCL:x+y=3 - 3"))
