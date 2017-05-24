with open("box.data", 'r') as file:
    for idx, line in enumerate(file.readlines()):
        if idx == 30:
            line = line.strip("\n").split(",")
            print(line)
