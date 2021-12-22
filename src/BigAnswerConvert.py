import VariableStuff
import EquationStuff


def bigConvert(someContent: str):

    someContent = someContent.replace("-", "-")
    someContent = someContent.replace("–", "-")
    someContent = someContent.replace("—", "-")
    # Dash-Hyphen(-), En-dash (–), Em-dash(—)
    # What how?

    if ":" in someContent:

        nameVar = someContent.strip().replace(" ", "").split(":")[0]
        data = someContent.strip().replace(" ", "").split(":")[-1]

        res = EquationStuff.convertAndCheck(data)
        if type(res) == type("hello"):
            return "Warning {} : {}".format(nameVar, res)

        return ("E", nameVar, data)
    elif "=" in someContent:
        nameVar = "=".join(someContent.strip().replace(" ", "").split("=")[:-1])
        dataStr = someContent.strip().replace(" ", "").split("=")[-1]
        data = VariableStuff.splitNumAndUnit(dataStr)

        if type(data) == type("error"):
            return "Warning {} : {}".format(nameVar, dataStr)

        val, unit = data
        if unit.strip() == "":
            return "Warning {} : {}".format(nameVar, "Unit not found")

        if unit[0] in "GMkmunp":
            if unit[0] == "G":
                val *= 1e9
            elif unit[0] == "M":
                val *= 1e6
            elif unit[0] == "k":
                val *= 1e3
            elif unit[0] == "m":
                val *= 1e-3
            elif unit[0] == "u":
                val *= 1e-6
            elif unit[0] == "n":
                val *= 1e-9
            elif unit[0] == "p":
                val *= 1e-12
            unit = unit[1:]

        return ("V", nameVar, val, unit)
    return ""


if __name__ == "__main__":

    def printWow(content):
        print("Type", content[0], content[1], "is", content[2], end=" ")

        if len(content) > 3:
            print(content[3])
        else:
            print()

    printWow(bigConvert("I1 = 1.2"))
    # printWow(bigConvert(""))
