def find(filename):
    for i in range(len(filename)):
        if filename[i] == ".":
            return i
    return len(filename)

