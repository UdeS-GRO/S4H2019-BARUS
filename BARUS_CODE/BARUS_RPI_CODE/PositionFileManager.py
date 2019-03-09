def initPositionDictionary(positionFilePath):
    posDict = {}
    file = open(positionFilePath, "r+")
    allPos = file.readlines()
    file.close()

    if len(allPos) > 0:
        for line in allPos:
            position = line.split()
            posDict[position[0]] = (position[1], position[2])
    return posDict


def saveNewPosition(key, posM1, posM2, posDict, positionFilePath):
    newTuple = (posM1, posM2)
    posDict[key] = newTuple

    file = open(positionFilePath, "w")
    for key in posDict:
        file.write(key + " " + str(posDict.get(key)[0]) + " " + str(posDict.get(key)[1]) + "\n")
    file.close()






