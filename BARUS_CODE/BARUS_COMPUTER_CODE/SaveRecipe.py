import os

curWorkDir = os.getcwd()
curWorkDir = curWorkDir.replace("\\", "/")     # Current working directory

def CreateRecipe(RecipeName):
    # Creates the new recipe position file
    newPosFile = curWorkDir + '/' + 'Recipes_List/' + RecipeName + '.txt'
    open(newPosFile,'a').close()
    currentRecipe = RecipeName # global variable
    #recipiesBank.append(RecipeName) # global list containing all existing