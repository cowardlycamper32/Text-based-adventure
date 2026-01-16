


dialogueFile = open("dialogue/player/01.dialogue")

instructions = dialogueFile.readlines()

responses = []

def runCMD(cmd, splitter = ":"):
    cmd = cmd.split(splitter)
    if cmd[0] == "TEXT":
        print(f"{cmd[1]} says {cmd[2]}")
    elif cmd[0] == "QUESTION":
        options = cmd[4].split(",")
        response = input(f"{cmd[1]} says {cmd[3]}")
        if response not in options:
            raise Exception(f"{response} not in {options}")
        responses.append({f"{cmd[2]}": response})
    elif cmd[0] == "IF":
        lookingFor = cmd[1]
        if cmd[2] == "IS":

            for j in responses:
                if lookingFor == list(j.keys())[0]:
                    print(f"{j[lookingFor]}: {cmd[3]}")
                    if j[lookingFor] == cmd[3]:
                        return runCMD(cmd[4], splitter=";")
        elif cmd[2] == "NOT":
            for j in responses:
                if lookingFor == list(j.keys())[0]:
                    print(f"not {j[lookingFor]}: {cmd[3]}")
                    if j[lookingFor] != cmd[3]:
                        return runCMD(cmd[4], splitter=";")
    elif cmd[0] == "GOTO":
        return int(cmd[1])


for q in range(2):
    running = True
    HEAD = 0

    while running:
        instruction = instructions[HEAD].strip()
        retVal = runCMD(instruction)
        if not retVal:
            HEAD = HEAD + 1
        else:
            HEAD = retVal - 1

        if HEAD >= len(instructions):
            running = False