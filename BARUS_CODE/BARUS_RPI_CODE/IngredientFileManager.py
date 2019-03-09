class Ingredient:
    def __init__(self, name, posM1):
        self.name = name
        self.posM1 = posM1


def initIngredientDictionary(ingredientFilePath):
    ingredientDict = {}
    file = open(ingredientFilePath, "r+")
    allIngredient = file.readlines()
    file.close()

    if len(allIngredient) > 0:
        for line in allIngredient:
            ingredient = line.split()
            ingredientDict[ingredient[0]] = Ingredient(ingredient[0], ingredient[1])
    return ingredientDict


def saveNewIngredient(name, posM1, ingredientDict, ingredientFilePath):
    ingredientDict[name] = Ingredient(name, posM1)

    file = open(ingredientFilePath, "w")
    for ingredient in ingredientDict:
        file.write(ingredient + " " + str(ingredientDict.get(ingredient).posM1) + "\n")
    file.close()

# path = "/home/pi/Desktop/IngredientFile"
# dict = initIngredientDictionary(path)

# saveNewIngredient("coke", 63 , dict , path)

# for key in dict:
#    print(key + " " + dict.get(key).name + " " + str(dict.get(key).posM1))


# for key in dict:
#    print(key + " " + str(dict.get(key)[0]) + " " + str(dict.get(key)[1]))


