def initPositionDictionary(positionFilePath):
    posDict = {}
    file = open(positionFilePath, "r+")
    allPos = file.readlines()
    file.close()

    if len(allPos) > 0:
        for line in allPos:
            position = line.split()
            posDict[position[0]] = (int(position[1]), int(position[2]), int(position[3]))
    return posDict


def saveNewPosition(key, posM1, posM2, qty, posDict, positionFilePath):
    newTuple = (posM1, posM2, qty)
    posDict[key] = newTuple

    file = open(positionFilePath, "w")
    for key in posDict:
        file.write(key + " " + str(posDict.get(key)[0]) + " " + str(posDict.get(key)[1]) + " " + str(posDict.get(key)[2]) + "\n")
    file.close()






