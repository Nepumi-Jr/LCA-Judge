import VariableStuff
import EquationStuff


def bigConvert(someContent: str):

    someContent = someContent.replace("-", "-")
    someContent = someContent.replace("–", "-")
    someContent = someContent.replace("—", "-")
    # Dash-Hyphen(-), En-dash (–), Em-dash(—)
    # What how?

    if ":" in someContent:

        nameVar = someContent.strip().replace(" ", '').split(":")[0]
        data = someContent.strip().replace(" ", '').split(":")[-1]

        res = EquationStuff.convertAndCheck(data)
        if type(res) == type("hello"):
            return "Warning {} : {}".format(nameVar, res)

        return ("E", nameVar, data)
    elif "=" in someContent:
        nameVar = "=".join(
            someContent.strip().replace(" ", '').split("=")[:-1])
        dataStr = someContent.strip().replace(" ", '').split("=")[-1]
        data = VariableStuff.splitNumAndUnit(dataStr)

        if type(data) == type("error"):
            return "Warning {} : {}".format(nameVar, dataStr)

        val, unit = data

        if unit[0] in "GMkmunp":
            if unit[0] == 'G':
                val *= 1e9
            elif unit[0] == 'M':
                val *= 1e6
            elif unit[0] == 'k':
                val *= 1e3
            elif unit[0] == 'm':
                val *= 1e-3
            elif unit[0] == 'u':
                val *= 1e-6
            elif unit[0] == 'n':
                val *= 1e-9
            elif unit[0] == 'p':
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

    printWow(bigConvert("I1 = 1.2 A"))
    printWow(bigConvert("Q1.1. magpp_vs = 20 V"))
    printWow(bigConvert("Q1.2. freq_vs = 400 Hz"))
    printWow(bigConvert("Q1.3. ZR = 100 ohm"))
    printWow(bigConvert("Q1.4. ZC = - j 198.943679092 ohm"))
    printWow(bigConvert("Q1.5. magpp_i = 0.089822 A"))
    printWow(bigConvert("Q1.6. freq_i = 400 Hz"))
    printWow(bigConvert("Q1.7. phase_i = 1.105027 rad"))
    printWow(bigConvert("Q1.8. phase_i = 63.31339 deg"))
    printWow(bigConvert("Q1.9. PR = 0.201699978039 W"))
    printWow(bigConvert("Q1.10. PC = 0 W"))
    printWow(bigConvert("I1 = 1.2 A"))
