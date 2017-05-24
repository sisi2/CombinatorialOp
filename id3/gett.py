with open("tennis.data", 'r') as file:
    for idx, line in enumerate(file.readlines()):
        if idx == 2:
            line = line.strip("\n").split(",")
            print(line)
