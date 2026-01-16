import os
import re
#from deprecated import deprecated

LETTERS = re.compile("[a-zA-Z]")

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



def text(cmd):
    """
    display text in terminal
    format expected: TEXT:<name>:<text>
    :param cmd: array of keywords used in command
    :return:
    """
    output = ["", ""]
    if "$" in cmd[1]:
        print("Var in Speaker Name")
        for j in variables:
            if cmd[1].strip("$") == list(j.keys())[0]:
                    output[1] = j.get(cmd[1].strip("$"))
            else:
                output[1] = j.get(cmd[1].strip("$"))
    else:
        output[1] = cmd[1]

    if "$" in cmd[2]:
        print("Var in TEXT")
        for j in variables:
            if cmd[2].strip("$") == list(j.keys())[0]:
                output[0] = j.get(cmd[2].strip("$"))
            else:
                output[0] = cmd[2]
    else:
        output[0] = cmd[2]
    print(output)
    print(f"{output[0]} says {output[1]}")

def question(cmd):
    """
    display question in terminal and store answer into variable system
    format expected: QUESTION:<name>:<var_name>:<var_type>:<text>:<option1>,<option2>,...
    :param cmd: array of keywords used in command
    :return:
    """
    options = cmd[5].split(",")
    response = input(f"{cmd[1]} says {cmd[4]}:\n")
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
    if cmd[2] == "IS":
        for j in variables:
            if lookingFor == list(j.keys())[0]:
                if j[lookingFor] == cmd[3]:
                    return runCMD(cmd[4], splitter=";")
    elif cmd[2] == "NOT":
        for j in variables:
            if lookingFor == list(j.keys())[0]:
                if j[lookingFor] != cmd[3]:
                    return runCMD(cmd[4], splitter=";")


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
        if j.get(cmd[2]):
            j[cmd[2]] = convert(cmd[3], cmd[1])
            return None

    if not (not cmd[3] or cmd[3] == ""):
        variables.append({cmd[2]: convert(cmd[3], cmd[1])})
    else:
        variables.append({cmd[2]: convert(None, cmd[1])})


def returncmd(cmd):
    if cmd[1] == "VARS":
        return variables
    for j in variables:
        if j.get(cmd[1]):
            return None
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



def runCMD(cmd, splitter = ":"):
    cmd = cmd.split(splitter)
    if cmd[0] == "TEXT":
        return text(cmd)
    elif cmd[0] == "QUESTION":
       return question(cmd)
    elif cmd[0] == "IF":
       return ifcmd(cmd)

    elif cmd[0] == "GOTO":
        return goto(cmd)
    elif cmd[0] == "VAR":
        return var(cmd)
    elif cmd[0] == "RETURN":
        print(returncmd(cmd))
    elif cmd[0] == "ADD":
        return add(cmd)
    elif cmd[0] == "MIN":
        return min(cmd)
    elif cmd[0] == "MUL":
        return mul(cmd)
    elif cmd[0] == "DIV":
        return div(cmd)
    elif cmd[0] == "CLEAR":
        clear(cmd)

dialogueFiles = os.scandir("dialogue")

for dialogueFilePath in dialogueFiles:
    dialogueFile = open(dialogueFilePath.path, "r")

    instructions = dialogueFile.readlines()

    variables = []

    running = True
    HEAD = 0

    while running:
        instruction = instructions[HEAD].strip()
        retVal = runCMD(instruction)
        #print(retVal)
        if not retVal:
            HEAD = HEAD + 1
        elif type(retVal) == int:
            HEAD = retVal - 1
        elif type(retVal) == Exception:
            print(f"{'\033[91m'}{retVal}{'\033[0m'}")
            if type(retVal) == ValueError or type(retVal) == TypeError or type(retVal) == NameError:
                exit()


        if HEAD >= len(instructions):
            running = False