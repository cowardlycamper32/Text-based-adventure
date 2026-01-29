import os
import re
import traceback
#from deprecated import deprecated

LETTERS = re.compile("[a-zA-Z]")
LOGLEVEL = 3

def convert(obj, type):
    if type == "STRING" or type == "STR":
        return str(obj)
    elif type == "INTEGER" or type == "INT":
        return int(obj)
    elif type == "FLOAT":
        return float(obj)
    elif type == "BOOLEAN" or type == "BOOL":
        return bool(obj)
    elif type is None:
        return obj
    else:
        return TypeError(f"Type {type} is not supported")



def text(cmd, delimiter="\n"):
    """
    display text in terminal
    format expected: TEXT:<name>:<text>
    :param cmd: array of keywords used in command
    :return:
    """
    output = ["", ""]
    nameWords = cmd[1].split(" ")
    for word in nameWords:
        if "$" in word:
            varb = getVar(word)
            output[1] += f"{varb["value"]} "
            break
        else:
            output[1] = cmd[1]

    speechWords = cmd[2].split(" ")
    for word in speechWords:
        if "$" in word:
            varb = getVar(word)
            output[0] += f"{varb["value"]} "
            break
        else:
            output[0] += f"{word} "
    print(f"{output[1]}:\n\t{output[0]}", end=delimiter)

def question(cmd):
    """
    display question in terminal and store answer into variable system
    format expected: QUESTION:<name>:<var_name>:<var_type>:<text>:<option1>,<option2>,...
    :param cmd: array of keywords used in command
    :return:
    """
    options = cmd[5].split(",")
    tempText = ["TEXT", cmd[1], cmd[4]]
    text(tempText, delimiter="")
    response = input()
    if response.lower() not in options:
        return Exception(f"{response} not in {options}")
    var(["", cmd[3], cmd[2], response])
    return None


def ifcmd(cmd):
    """
    evaluate things
    format expected: IF:<var>:<IS|NOT>:<text>:<cmd if true>
    :param cmd:
    :return:
    """
    lookingFor = cmd[1]

    output = ["", ""]
    nameWords = cmd[3].split(" ")
    for word in nameWords:
        if "$" in word:
            varb = getVar(word)
            output[1] += f"{convert(varb['value'], varb['type'])} "
            break
        else:
            output[1] = f"{word} "

    speechWords = cmd[1].split(" ")
    for word in speechWords:
        if "$" in word:
            varb = getVar(word)
            output[0] += f"{convert(varb['value'], varb['type'])} "
            break
        else:
            output[0] += f"{word} "



    match cmd[2]:
        case "==":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"])  == convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case "!=":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"]) != convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case ">":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"]) > convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case "<":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"]) < convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case ">=":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"]) >= convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case "<=":
            varb = getVar(lookingFor)
            if convert(varb["value"], varb["type"]) <= convert(cmd[3], varb['type']):
                return runCMD(cmd[4], splitter=";")
        case _:
            return ValueError(f"operator {cmd[2]} is not supported")



def convertPyTypes(typeb: type):
    if typeb == str:
        return "STRING"
    elif typeb == int:
        return "INTEGER"
    elif typeb == bool:
        return "BOOLEAN"
    elif typeb == float:
        return "FLOAT"

def goto(cmd):
    """
    Go to line number
    :param cmd:
    :return:
    """
    return int(cmd[1])


def var(cmd):
    """
    define or assign variable
    format expected: VAR:<var_type>:<var_name>:<value>
    :param cmd:
    :return:
    """
    for j in variables:
        varVal = j.get(cmd[1])

        #if not isinstance(varVal, bool):
        #    if not (not cmd[3] or cmd[3] == ""):
        #        j[cmd[2]] == convert(None, cmd[1])
        #    j[cmd[2]] = convert(cmd[3], cmd[1])
        #    return None

    varConstructor = {}

    if not (not cmd[3] or cmd[3] == ""):
        varConstructor["name"] = cmd[2]
        varConstructor["type"] = cmd[1]
        varConstructor["value"] = cmd[3]
        variables.append(varConstructor)
    else:
        varConstructor["name"] = cmd[2]
        varConstructor["type"] = cmd[1]
        varConstructor["value"] = None
        variables.append(varConstructor)
    return None


def returncmd(cmd):
    if cmd[1] == "VARS":
        return variables
    nameWords = cmd[1].split(" ")
    output = ""
    for word in nameWords:
        if "$" in word:
            for j in variables:
                if word.strip("$") == list(j.keys())[0]:
                    output += str(j.get(cmd[1].strip("$")))
                    return output
        else:
            output = cmd[1]
            return output
    return NameError(f"variable {cmd[1]} does not exist")

def add(cmd):
    numbs = cmd[1].split(",")
    values = []
    for i in numbs:
        if not LETTERS.match(str(i)):
            values.append(int(i))
        else:
            for j in variables:
                if i == list(j.keys())[0]:
                    values.append(int(j.get(i)))
                    break

    total = 0

    for i in values:
        total += i

    var(["", "INT", cmd[2], total])

def min(cmd):
    numbs = cmd[1].split(",")
    values = []
    total = 0
    for i in numbs:
        if not LETTERS.match(str(i)):
            values.append(int(i))
        else:
            for j in variables:
                if i == list(j.keys())[0]:
                    values.append(int(j.get(i)))



    total = values[0]
    values.pop(0)
    for i in values:
        total -= i

    var(["", "INT", cmd[2], total])

def mul(cmd):
    numbs = cmd[1].split(",")
    values = []
    for i in numbs:
        if not LETTERS.match(str(i)):
            values.append(int(i))
        else:
            for j in variables:
                if i == list(j.keys())[0]:
                    values.append(int(j.get(i)))

    total = values[0]
    values.pop(0)
    for i in values:
        total *= i

    var(["", "INT", cmd[2], total])

def div(cmd):
    numbs = cmd[1].split(",")
    values = []
    for i in numbs:
        if not LETTERS.match(str(i)):
            values.append(int(i))
        else:
            for j in variables:
                if i == list(j.keys())[0]:
                    values.append(int(j.get(i)))

    total = values[0] / values[1]

    var(["", "INT", cmd[2], total])

def clear(cmd):
    for j in range(len(variables)):
        if cmd[1] == list(variables[j - 1].keys())[0]:
            variables.pop(j - 1)
            return None
    return ValueError(f"variable {cmd[1]} does not exist")

def modulo(cmd):
    """
    modulo function, expects ["MOD", x, y, <var_name>]
    :param cmd:
    :return:
    """
    numbs = cmd[1].split(",")
    vara = getVar(numbs[0])
    varb = getVar(numbs[1])
    try:
        out = convert(vara["value"], vara["type"]) % convert(varb["value"], varb["type"])
        var(["", vara["type"], cmd[2], out])
    except ValueError:
        return ValueError(f"attempted to modulo veriables of types {vara['type']}, {varb['type']}")

def getVar(var):
    for j in variables:
        if var.strip("$") == j.get("name"):
            return j
    out = {}
    out["value"] = var
    if LETTERS.match(str(var)):
        typed = str
    else:
        typed = int

    out["type"] = convertPyTypes(typed)
    return out

def runCMD(cmd, splitter = ":"):
    if cmd == "":
        return None
    cmd = cmd.split(splitter)

    match cmd[0]:
        case "TEXT":
            return text(cmd)
        case "QUESTION":
            return question(cmd)
        case "IF":
            return ifcmd(cmd)
        case "GOTO":
            return goto(cmd)
        case "VAR":
            return var(cmd)
        case "RETURN":
            print(returncmd(cmd))
            return None
        case "CLEAR":
            return clear(cmd)

        # MATH functions
        case "ADD":
            return add(cmd)
        case "MIN":
            return min(cmd)
        case "MUL":
            return mul(cmd)
        case "DIV":
            return div(cmd)

        case "//":
            return None
        case "MOD":
            return modulo(cmd)

        case _:
            raise ValueError(f"unknown command: {cmd[0]} at line {HEAD + 1}")

dialogueFiles = os.scandir("dialogue")

for dialogueFilePath in dialogueFiles:
    dialogueFile = open(dialogueFilePath.path, "r")

    instructions = dialogueFile.readlines()

    variables = []

    running = True
    HEAD = 0
    try:
        while running:
            instruction = instructions[HEAD].strip()
            retVal = runCMD(instruction)
            #print(retVal)
            if not retVal:
                HEAD = HEAD + 1
            elif type(retVal) == int:
                HEAD = retVal - 1
            elif isinstance(retVal, Exception):
                print(f"{'\033[91m'}{retVal}{'\033[0m'}")
                if LOGLEVEL >= 3:
                    print(f"{'\033[91m'}{traceback.format_exc()}{'\033[0m'}")
                if type(retVal) == ValueError or type(retVal) == TypeError or type(retVal) == NameError:
                    exit()



        if HEAD >= len(instructions):
            running = False
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            print(f"\n{'\033[91m'}Execution Finished.{'\033[0m'}")
        else:
            print(f"{'\033[91m'}Internal Engine Exception '{type(e).__name__}' occurred at line \"{HEAD+1}\" with message '{e}'{'\033[0m'}")
        if LOGLEVEL >= 3:
            print(f"{'\033[91m'}{traceback.format_exc()}{'\033[0m'}")
