import IngredientFileManager


class Recipe:

    def __init__(self, name, listOfIngredient):
        self.name = name
        self.listOfIngredient = listOfIngredient

    def getIngredients(self):
        ingrdIndex = 0
        qtyIndex = 1
        if len(self.listOfIngredient) > 0:
            print("The repipe for " + self.name + " is:")
            print("Ingredient\tQuantity")

            for ingredient in self.listOfIngredient:
                print(ingredient[ingrdIndex].name + "\t\t" + str(ingredient[qtyIndex]))


recetteTest = []
rhum = IngredientFileManager.Ingredient("Rhum", 654)
coke = IngredientFileManager.Ingredient("Coke", 987)

recetteTest.append((rhum, 2))
recetteTest.append((coke, 8))

RhumNCoke = Recipe("Rhum-N-Coke", recetteTest)

RhumNCoke.getIngredients()

