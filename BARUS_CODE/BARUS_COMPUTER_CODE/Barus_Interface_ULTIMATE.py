# This is the code for the Barus interface in python.
# Created by Olivier Girouard, 08/03/2019
# Updated by William Aris and Olivier Girouard

# we are using wxPython:
import wx
import os
import wx.lib.filebrowsebutton
import Gripper
from Constant import *
from SerialCom import *
from PositionFileManager import *
from Motor import *
from SaveRecipe import *
import time

app = wx.App()

curWorkDir = os.getcwd()
curWorkDir = curWorkDir.replace("\\", "/")     # Current working directory
RecipeListDir = curWorkDir + "/Recipes_List/"  # Directory for recipes list

DrinkOrderDisplay = ""  # The displayed order in the "OrderADrink" window
SelectedRecipe = ""     # The Selected recipe by the user in the "ListOfRecipes" window

statesIndex = 0    # Index to choose the tag of a position
statesBank = ["HOME", "INGREDIENT_1", "INGREDIENT_2", "INGREDIENT_3"]   # List of tags
state = statesBank[statesIndex]     # Current tag
recipesBank = []
currentRecipe = "RHUM_AND_COKE"

class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, size=(1280, 720), style=wx.SYSTEM_MENU)

        self.Center()

        # Text
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        # pictures
        background = wx.StaticBitmap(self)
        background.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/Home_Background.png"))

        # Buttons
        orderButtonLogo = wx.Image(curWorkDir + "/pictures/order_button.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.BtnOrderDrink = wx.BitmapButton(background, -1, orderButtonLogo, pos=(396, 450))
        moveButtonLogo = wx.Image(curWorkDir + "/pictures/move_button.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.BtnManualCtrl = wx.BitmapButton(background, -1, moveButtonLogo, pos=(689, 450))
        ExitIcon = wx.Image(curWorkDir + "/pictures/ExitBtnV3.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.closeButton = wx.BitmapButton(background, -1, ExitIcon, pos=(1035, 20), )

        # Setting up the menu.
        windowMenu= wx.Menu()
        menuAbout = windowMenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        menuExit = windowMenu.Append(wx.ID_EXIT, "&Exit", " Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(windowMenu, "&File")
        self.SetMenuBar(menuBar)                       # Adding the MenuBar to the window
        self.Show()

        # Set events                                   # We bind objects to an event using Bind()
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.BtnManualCtrl.Bind(wx.EVT_BUTTON, self.openManualCtrl)
        self.BtnOrderDrink.Bind(wx.EVT_BUTTON, self.OpenOrderADrink)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnExit)

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "This is the Barus Interface\n\nLast update: 13/03/2019",
                                        "About this application", wx.ICON_NONE)

        dlg.ShowModal()   # Show it
        dlg.Destroy()     # finally destroy it when finished.

    def OnExit(self, event):
        YesNoBox = wx.MessageDialog(self, "You are about to quit\n\n\
                    Are you sure you want to leave now?", "Before leaving", wx.CANCEL | wx.CANCEL_DEFAULT)
        answer = YesNoBox.ShowModal()   # Show it

        if answer == wx.ID_OK:
            self.Close()            # Close the frame.

        YesNoBox.Destroy()          # finally destroy it when finished.

    def openManualCtrl(self, event):
        print("Button clicked, opening Manual control window")
        MoveRobotFrame(None)
        mainWindow.Hide()

    def OpenOrderADrink(self, event):
        print("Button clicked, opening the window to order a drink")
        OrderADrinkFrame(None)
        mainWindow.Hide()

class RecipeNamerFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(1100, 480), title="Recipe's Name", style= wx.SYSTEM_MENU | wx.CAPTION )

        panel = wx.Panel(self)
        self.Center()

        # Picture
        background = wx.StaticBitmap(panel, pos=(0, 0))
        background.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/recipes_naming_background.png"))

        #Text
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.nameField = wx.TextCtrl(background, -1, pos=(490, 250), size=(440, 25))
        self.nameField.SetFont(font)

        #Buttons
        fontButtons = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.OKButton = wx.Button(background, label="OK", pos=(720,290), size = (150, 50))
        self.OKButton.SetFont(fontButtons)

        self.cancelButton = wx.Button(background, label="Cancel", pos=(560, 290), size=(150, 50))
        self.cancelButton.SetFont(fontButtons)

        #Events
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        self.OKButton.Bind(wx.EVT_BUTTON, self.OnOKButton)

        self.Show()

    def OnOKButton(self, event):
        global currentRecipe

        CreateRecipe(self.nameField.GetValue()) # Create a recipe file with the name given by the text box
        currentRecipe = self.nameField.GetValue()
        CreationFrame(None) # Open the creation frame
        mainWindow.Hide()
        self.Destroy()

    def OnCancelButton(self, event):
        self.Destroy()

class CreationFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, size=(1280, 720), style=wx.SYSTEM_MENU)

        self.Center()

        panel = wx.Panel(self)

        # Pictures
        titlePicture = wx.StaticBitmap(panel, pos=(320, 0))
        titlePicture.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/recipe_window_title.png"))

        curPosTable = wx.StaticBitmap(panel, pos=(53, 130))
        curPosTable.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/current_pos_table.png"))

        savedPosTable = wx.StaticBitmap(panel, pos=(448, 130))
        savedPosTable.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/saved_pos_table.png"))

        moveRobotTable = wx.StaticBitmap(panel, pos=(843, 130))
        moveRobotTable.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/move_robot_table.png"))

        # Buttons Pictures
        upArrow = wx.Image(curWorkDir + "/pictures/up_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        downArrow = wx.Image(curWorkDir + "/pictures/down_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        rightArrow = wx.Image(curWorkDir + "/pictures/right_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        leftArrow = wx.Image(curWorkDir + "/pictures/left_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        openBMP = wx.Image(curWorkDir + "/pictures/open_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        closeBMP = wx.Image(curWorkDir + "/pictures/close_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()

        savePosBMP = wx.Image(curWorkDir + "/pictures/save_pos_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        resetPosBMP = wx.Image(curWorkDir + "/pictures/reset_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()

        # Buttons
        self.openBtn = wx.BitmapButton(moveRobotTable, -1, openBMP, pos=(20, 130))
        self.closeBtn = wx.BitmapButton(moveRobotTable, -1, closeBMP, pos=(255, 130))
        self.leftBtn_J2 = wx.BitmapToggleButton(moveRobotTable, -1, downArrow, pos=(20, 255))
        self.rightBtn_J2 = wx.BitmapToggleButton(moveRobotTable, -1, upArrow, pos = (255,255))
        self.leftBtn_J1 = wx.BitmapToggleButton(moveRobotTable, -1, leftArrow, pos=(20, 380))
        self.rightBtn_J1 = wx.BitmapToggleButton(moveRobotTable, -1, rightArrow, pos = (255, 380))

        self.savePosBtn = wx.BitmapButton(savedPosTable, -1, savePosBMP, pos=(190, 410))
        self.resetBtn = wx.BitmapButton(savedPosTable, -1, resetPosBMP, pos=(35, 155))

        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.BtnReturnHome = wx.Button(panel, label="Return to Home", pos=(30, 20), size=(200, 50))
        self.BtnReturnHome.SetFont(font2)

        self.stopButton = wx.Button(panel, label="Emergency Stop", pos =(1050, 20), size=(200, 50))
        self.stopButton.SetFont(font2)
        self.stopButton.SetFocus()

        # Drop Down Lists
        quantityChoices = ['0 Oz', '1 Oz', '2 Oz']
        self.quantityList = wx.Choice(savedPosTable, pos = (20,425), size = (163,200), choices = quantityChoices)
        font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.quantityList.SetFont(font)
        self.quantityList.SetSelection(0)

        # Text
        self.stateTxt = wx.TextCtrl(panel, value = state, pos = (624,230), size = (173, 43), style = wx.TE_READONLY|wx.TE_CENTER)
        self.stateTxt.SetFont(font)

        self.gripperTxt = wx.TextCtrl(panel, value = "OPEN", pos = (245,274), size = (126,43), style = wx.TE_READONLY|wx.TE_CENTER)
        self.gripperTxt.SetFont(font)

        self.motor1Txt = wx.TextCtrl(panel, value = str(0), pos = (245,538), size = (126,43), style = wx.TE_READONLY|wx.TE_CENTER)
        self.motor1Txt.SetFont(font)

        self.motor2Txt = wx.TextCtrl(panel, value = str(0), pos = (245,406), size = (127,43), style = wx.TE_READONLY|wx.TE_CENTER)
        self.motor2Txt.SetFont(font)

        # Setting up the menu.
        windowMenu = wx.Menu()
        menuAbout = windowMenu.Append(wx.ID_ABOUT, "&About", " Information about this window")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(windowMenu, "&File")
        self.SetMenuBar(menuBar)

        # Events
        self.leftBtn_J2.Bind(wx.EVT_TOGGLEBUTTON, self.leftTurn_J2)
        self.rightBtn_J2.Bind(wx.EVT_TOGGLEBUTTON, self.rightTurn_J2)
        self.leftBtn_J1.Bind(wx.EVT_TOGGLEBUTTON, self.leftTurn_J1)
        self.rightBtn_J1.Bind(wx.EVT_TOGGLEBUTTON, self.rightTurn_J1)
        self.openBtn.Bind(wx.EVT_BUTTON, self.openBtnPressed)
        self.closeBtn.Bind(wx.EVT_BUTTON, self.closeBtnPressed)

        self.savePosBtn.Bind(wx.EVT_BUTTON, self.savePosBtnPressed)
        self.resetBtn.Bind(wx.EVT_BUTTON, self.resetPosBtnPressed)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.BtnReturnHome.Bind(wx.EVT_BUTTON, self.goToHome)

        self.stopButton.Bind(wx.EVT_KEY_DOWN, self.emergencyStop)
        self.stopButton.Bind(wx.EVT_BUTTON, self.emergencyStop)

        self.Show()


    def rightTurn_J2(self, event):
        print("J2 Right")

        buttonState = event.GetEventObject().GetValue()
        self.leftBtn_J2.SetValue(False)

        if buttonState == True:
            rotateClockWise(MOTOR_2_WHEEL)

        else:
            rotateStop(MOTOR_2_WHEEL)
            motorPosition = readMotorPosition()
            self.motor2Txt.SetValue(str(motorPosition[1]))

        self.stopButton.SetFocus()

    def leftTurn_J2(self, event):
        print("J2 Left")

        buttonState = event.GetEventObject().GetValue()
        self.rightBtn_J2.SetValue(False)

        if buttonState == True:
            rotateCounterClockWise(MOTOR_2_WHEEL)

        else:
            rotateStop(MOTOR_2_WHEEL)
            motorPosition = readMotorPosition()
            self.motor2Txt.SetValue(str(motorPosition[1]))

        self.stopButton.SetFocus()

    def rightTurn_J1(self, event):
        print("J1 Right")

        buttonState = event.GetEventObject().GetValue()
        self.leftBtn_J1.SetValue(False)

        if buttonState == True:
            rotateCounterClockWise(MOTOR_1_WHEEL)
        else:
            rotateStop(MOTOR_1_WHEEL)
            motorPosition = readMotorPosition()
            self.motor1Txt.SetValue(str(motorPosition[0]))

        self.stopButton.SetFocus()

    def leftTurn_J1(self, event):
        print("J1 Left")

        buttonState = event.GetEventObject().GetValue()
        self.rightBtn_J1.SetValue(False)

        if buttonState == True:
            rotateClockWise(MOTOR_1_WHEEL)
        else:
            rotateStop(MOTOR_1_WHEEL)
            motorPosition = readMotorPosition()
            self.motor1Txt.SetValue(str(motorPosition[0]))

        self.stopButton.SetFocus()

    def openBtnPressed(self,event):
        print("Gripper Open")
        Gripper.openGripper()
        self.gripperTxt.SetValue("OPEN")

        self.stopButton.SetFocus()

    def closeBtnPressed(self, event):
        print("Gripper Close")
        Gripper.closeGripper()
        self.gripperTxt.SetValue("CLOSE")

        self.stopButton.SetFocus()

    def emergencyStop(self, event):
        rotateStop(MOTOR_1_WHEEL)
        rotateStop(MOTOR_2_WHEEL)
        self.rightBtn_J1.SetValue(False)
        self.leftBtn_J1.SetValue(False)
        self.rightBtn_J2.SetValue(False)
        self.leftBtn_J2.SetValue(False)

        motorPosition = readMotorPosition()
        self.motor2Txt.SetValue(str(motorPosition[1]))
        self.motor1Txt.SetValue(str(motorPosition[0]))

    def savePosBtnPressed(self, event):
        print("Save Position")

        global state
        global statesBank
        global statesIndex
        global currentRecipe

        positions = readMotorPosition()

        if positions[0] >= 0 and positions[1] >= 0:
            positionFilePath = os.getcwd() + "/" + "Recipes_List/" + currentRecipe + ".txt"
            positionFilePath = positionFilePath.replace("\\", "/")
            posDict = initPositionDictionary(positionFilePath)

            if state == "INGREDIENT_1" or state == "INGREDIENT_2" or state == "INGREDIENT_3":
                saveNewPosition(state, positions[0], positions[1], self.quantityList.GetSelection(), posDict, positionFilePath)
            else:
                saveNewPosition(state, positions[0], positions[1], 0, posDict, positionFilePath)

            statesIndex += 1

            if statesIndex >= len(statesBank):
                statesIndex = 0

            state = statesBank[statesIndex]
            self.stateTxt.SetValue(state)

        self.stopButton.SetFocus()

    def resetPosBtnPressed(self, evt):
        global state
        global statesBank
        global statesIndex

        statesIndex = 0

        state = statesBank[statesIndex]
        self.stateTxt.SetValue(state)

        self.stopButton.SetFocus()

    def goToHome(self, event):
        print("button pressed")
        self.Close()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "This is the window to control Barus manually\n\nLast update: 08/03/2019",
                                        "About this window", wx.ICON_NONE)

        dlg.ShowModal()   # Show it
        dlg.Destroy()     # finally destroy it when finished.

class MoveRobotFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, size=(1280, 720), style=wx.SYSTEM_MENU)

        self.Center()

        background = wx.StaticBitmap(self)
        background.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/move_background-v2.png"))

        # Buttons Pictures
        upArrow = wx.Image(curWorkDir + "/pictures/up_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        downArrow = wx.Image(curWorkDir + "/pictures/down_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        rightArrow = wx.Image(curWorkDir + "/pictures/right_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        leftArrow = wx.Image(curWorkDir + "/pictures/left_arrow.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        openBMP = wx.Image(curWorkDir + "/pictures/open_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        closeBMP = wx.Image(curWorkDir + "/pictures/close_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()

        # Buttons
        self.leftBtn_J2 = wx.BitmapToggleButton(background, -1, downArrow, pos=(705, 410))
        self.rightBtn_J2 = wx.BitmapToggleButton(background, -1, upArrow, pos=(945, 410))
        self.leftBtn_J1 = wx.BitmapToggleButton(background, -1, leftArrow, pos=(705, 530))
        self.rightBtn_J1 = wx.BitmapToggleButton(background, -1, rightArrow, pos=(945, 530))

        self.openBtn = wx.BitmapButton(background, -1, openBMP, pos=(705, 280))
        self.closeBtn = wx.BitmapButton(background, -1, closeBMP, pos=(940, 280))

        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self.stopButton = wx.Button(background, label="Emergency Stop", pos=(1040, 20), size=(200, 50))
        self.stopButton.SetFont(font2)
        self.stopButton.SetFocus()

        ReturnHome = wx.Image(curWorkDir + "/pictures/Return_To_Home.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.BtnReturnHome = wx.BitmapButton(background, -1, ReturnHome, pos=(30, 20), )

        # Font
        font = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        # Text
        self.gripperTxt = wx.TextCtrl(background, value="OPEN", pos=(384, 282), size=(126, 43),
                                      style=wx.TE_READONLY | wx.TE_CENTER)
        self.motor1Txt = wx.TextCtrl(background, value=str(0), pos=(384, 548), size=(127, 43),
                                     style=wx.TE_READONLY | wx.TE_CENTER)
        self.motor2Txt = wx.TextCtrl(background, value=str(0), pos=(384, 415), size=(126, 43),
                                     style=wx.TE_READONLY | wx.TE_CENTER)
        self.gripperTxt.SetFont(font)
        self.motor1Txt.SetFont(font)
        self.motor2Txt.SetFont(font)


        # Setting up the menu.
        windowMenu = wx.Menu()
        menuAbout = windowMenu.Append(wx.ID_ABOUT, "&About", " Information about this window")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(windowMenu, "&File")
        self.SetMenuBar(menuBar)

        # Events
        self.leftBtn_J2.Bind(wx.EVT_TOGGLEBUTTON, self.leftTurn_J2)
        self.rightBtn_J2.Bind(wx.EVT_TOGGLEBUTTON, self.rightTurn_J2)
        self.leftBtn_J1.Bind(wx.EVT_TOGGLEBUTTON, self.leftTurn_J1)
        self.rightBtn_J1.Bind(wx.EVT_TOGGLEBUTTON, self.rightTurn_J1)
        self.openBtn.Bind(wx.EVT_BUTTON, self.openBtnPressed)
        self.closeBtn.Bind(wx.EVT_BUTTON, self.closeBtnPressed)

        self.stopButton.Bind(wx.EVT_KEY_DOWN, self.emergencyStop)
        self.stopButton.Bind(wx.EVT_BUTTON, self.emergencyStop)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.BtnReturnHome.Bind(wx.EVT_BUTTON, self.goToHome)

        self.Show()

    def rightTurn_J2(self, event):
        print("J2 Right")

        buttonState = event.GetEventObject().GetValue()
        self.leftBtn_J2.SetValue(False)

        if buttonState == True:
            rotateClockWise(MOTOR_2_WHEEL)

        else:
            rotateStop(MOTOR_2_WHEEL)
            motorPosition = readMotorPosition()
            self.motor2Txt.SetValue(str(motorPosition[1]))

        self.stopButton.SetFocus()

    def leftTurn_J2(self, event):
        print("J2 Left")

        buttonState = event.GetEventObject().GetValue()
        self.rightBtn_J2.SetValue(False)

        if buttonState == True:
            rotateCounterClockWise(MOTOR_2_WHEEL)
        else:
            rotateStop(MOTOR_2_WHEEL)
            motorPosition = readMotorPosition()
            self.motor2Txt.SetValue(str(motorPosition[1]))

        self.stopButton.SetFocus()

    def rightTurn_J1(self, event):
        print("J1 Right")

        buttonState = event.GetEventObject().GetValue()
        self.leftBtn_J1.SetValue(False)

        if buttonState == True:
            rotateCounterClockWise(MOTOR_1_WHEEL)
        else:
            rotateStop(MOTOR_1_WHEEL)
            motorPosition = readMotorPosition()
            self.motor1Txt.SetValue(str(motorPosition[0]))

        self.stopButton.SetFocus()

    def leftTurn_J1(self, event):
        print("J1 Left")

        buttonState = event.GetEventObject().GetValue()
        self.rightBtn_J1.SetValue(False)

        if buttonState == True:
            rotateClockWise(MOTOR_1_WHEEL)
        else:
            rotateStop(MOTOR_1_WHEEL)
            motorPosition = readMotorPosition()
            self.motor1Txt.SetValue(str(motorPosition[0]))

        self.stopButton.SetFocus()

    def openBtnPressed(self, event):
        print("Gripper Open")
        Gripper.openGripper()
        self.gripperTxt.SetValue("OPEN")

        self.stopButton.SetFocus()

    def closeBtnPressed(self, event):
        print("Gripper Close")
        Gripper.closeGripper()
        self.gripperTxt.SetValue("CLOSE")

        self.stopButton.SetFocus()

    def emergencyStop(self, event):
        print("STOP")
        rotateStop(MOTOR_1_WHEEL)
        rotateStop(MOTOR_2_WHEEL)
        self.rightBtn_J1.SetValue(False)
        self.leftBtn_J1.SetValue(False)
        self.rightBtn_J2.SetValue(False)
        self.leftBtn_J2.SetValue(False)

        motorPosition = readMotorPosition()
        self.motor2Txt.SetValue(str(motorPosition[1]))
        self.motor1Txt.SetValue(str(motorPosition[0]))

    def goToHome(self, event):
        print("button pressed")
        self.Close()
        mainWindow.Show()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "This is the window to control Barus manually\n\nLast update: 08/03/2019",
                               "About this window", wx.ICON_NONE)

        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

class OrderADrinkFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(1280, 720), style=wx.SYSTEM_MENU)

        #panel = wx.Panel(self)

        # background
        background = wx.StaticBitmap(self)
        background.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/Order_Background_V4.v1.png"))

        # Text font
        font1 = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        font2 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font3 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font4 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        # Buttons

        ReturnHome = wx.Image(curWorkDir + "/pictures/Return_To_Home.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.BtnReturnHome = wx.BitmapButton(background, -1, ReturnHome, pos=(30, 20), )
        recipeList = wx.Image(curWorkDir + "/pictures/List_of_Recipes_btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        confirm = wx.Image(curWorkDir + "/pictures/Confirm_Order_Btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        CreateDrink = wx.Image(curWorkDir + "/pictures/Create_Recipe_Btn.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.BtnRecipeList = wx.BitmapButton(background, -1, recipeList, pos=(110, 300))
        self.CreateDrink = wx.BitmapButton(background, -1, CreateDrink, pos=(110, 480))
        self.BtnConfirm = wx.BitmapButton(background, -1, confirm, pos=(230, 600))
        self.BtnConfirm.Hide()  # as long as the box "Your Order" is not filled

        # Text Box
        self.OrderDisplay = wx.TextCtrl(background, -1, pos=(720, 200), size=(452, 145), style=wx.TE_MULTILINE)
        self.OrderDisplay.SetFont(font3)
        global DrinkOrderDisplay
        self.OrderDisplay.Value = DrinkOrderDisplay

        # Setting up the menu.
        windowMenu = wx.Menu()
        menuAbout = windowMenu.Append(wx.ID_ABOUT, "&About", " Information about this window")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(windowMenu, "&File")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the window

        # events
        self.BtnReturnHome.Bind(wx.EVT_BUTTON, self.goToHome)
        self.BtnRecipeList.Bind(wx.EVT_BUTTON, self.OpenRecipeList)
        self.CreateDrink.Bind(wx.EVT_BUTTON, self.OpenCreateDrinkWindow)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.BtnConfirm.Bind(wx.EVT_BUTTON, self.ConfirmOrder)

        self.Center()
        self.Show()

    def OpenRecipeList(self, event):
        global DrinkOrderDisplay
        global currentRecipe
        print("Open Recipe List")
        RecipeListBrowser = ListOfRecipes(self)  # this class is now the parent of ListOfRecipes
        DrinkOrderDisplay = ""
        currentRecipe = ""

    def OpenCreateDrinkWindow(self,event):
        print("Open Create drink window")
        RecipeNamerFrame(None)


    def ConfirmOrder(self, event):
        global DrinkOrderDisplay
        global currentRecipe

        print("Order confirmed")

        # Getting the selection's position file
        # choiceIndex = self.listeDeroulante.GetSelection()
        # drinkChoice = self.listeDeroulante.GetString(choiceIndex)
        drinkFilePath = os.getcwd() + "/" + "Recipes_List/" + currentRecipe

        # Initiating de positions dictionary
        posDict = initPositionDictionary(drinkFilePath)

        # Extracting positions
        homePos = (posDict["HOME"][0], posDict["HOME"][1])
        # pickCup = (posDict[PICK_UP][1], posDict[PICKUP][2])
        firstIngredient = (posDict["INGREDIENT_1"][0], posDict["INGREDIENT_1"][1])
        secondIngredient = (posDict["INGREDIENT_2"][0], posDict["INGREDIENT_2"][1])
        thirdIngredient = (posDict["INGREDIENT_3"][0], posDict["INGREDIENT_3"][1])
        # dropCup = (posDict[DROP][1], posDict[DROP][2])

        # Extracting
        firstIngredientQty = posDict["INGREDIENT_1"][2]
        secondIngredientQty = posDict["INGREDIENT_2"][2]
        thirdIngredientQty = posDict["INGREDIENT_3"][2]

        # Preparing Drink

        # Adjust Arm Height and open gripper
        turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)
        Gripper.openGripper()

        # Home position
        turnToPos(MOTOR_1_JOINT, homePos[0])
        time.sleep(WAIT)
        turnToPos(MOTOR_2_JOINT, homePos[1])
        time.sleep(WAIT)
        Gripper.closeGripper()
        time.sleep(WAIT)

        # First ingredient
        if (firstIngredientQty != 0):

           # Approach
            turnToPos(MOTOR_1_JOINT, firstIngredient[0])
            time.sleep(WAIT)
            turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)
            time.sleep(WAIT)

            # First Ingredient
            if (firstIngredientQty == 1):
                turnToPos(MOTOR_2_JOINT, firstIngredient[1])
                time.sleep(POUR_1OZ)
            else:
                turnToPos(MOTOR_2_JOINT, firstIngredient[1])
                time.sleep(POUR_1OZ)
                turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)
                time.sleep(WAIT_SHOT)
                turnToPos(MOTOR_2_JOINT, firstIngredient[1])
                time.sleep(POUR_1OZ)

            # Retreat
            turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)

        # Second ingredient
        if (secondIngredientQty != 0):
            # Approach
            turnToPos(MOTOR_1_JOINT, secondIngredient[0])
            time.sleep(WAIT)

            # Second Ingredient
            if (secondIngredientQty == 1):
                turnToPos(MOTOR_2_JOINT, secondIngredient[1])
                time.sleep(POUR_1OZ)
            else:
                turnToPos(MOTOR_2_JOINT, secondIngredient[1])
                time.sleep(POUR_1OZ)
                turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)
                time.sleep(WAIT_SHOT)
                turnToPos(MOTOR_2_JOINT, secondIngredient[1])
                time.sleep(POUR_1OZ)

            # Retreat
            turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)

        # Third ingredient
        if (thirdIngredientQty != 0):
            # Approach
            turnToPos(MOTOR_1_JOINT, thirdIngredient[0])
            time.sleep(WAIT)

            # Second Ingredient
            if (thirdIngredientQty == 1):
                turnToPos(MOTOR_2_JOINT, thirdIngredient[1])
                time.sleep(POUR_1OZ)
            else:
                turnToPos(MOTOR_2_JOINT, thirdIngredient[1])
                time.sleep(POUR_1OZ)
                turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)
                time.sleep(WAIT_SHOT)
                turnToPos(MOTOR_2_JOINT, thirdIngredient[1])
                time.sleep(POUR_1OZ)


            # Retreat
            turnToPos(MOTOR_2_JOINT,DEF_HEIGHT)

        # Drop cup
        turnToPos(MOTOR_1_JOINT, homePos[0])
        time.sleep(WAIT)
        turnToPos(MOTOR_2_JOINT, homePos[1])
        time.sleep(WAIT)
        Gripper.openGripper()
        time.sleep(WAIT)
        turnToPos(MOTOR_2_JOINT, DEF_HEIGHT)

        # We reset variables before the next command:
        DrinkOrderDisplay = ""
        currentRecipe = ""

    def goToHome(self, event):
        print("button pressed")
        self.Close()
        mainWindow.Show()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "This is the window to order a drink\n\nLast update: 09/04/2019",
                                        "About this application", wx.ICON_NONE)

        dlg.ShowModal()   # Show it
        dlg.Destroy()     # finally destroy it when finished.

    def UpdateOrderDisplay(self):  # Called by the ListOfRecipes window to update the "your Order" TextCtrl
        self.OrderDisplay.Value = DrinkOrderDisplay
        if DrinkOrderDisplay != "":  # Show Confirm button
            self.BtnConfirm.Show()

class ListOfRecipes(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(600, 300), title="List of recipes", style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                                                         wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.ICON_NONE)

        self.parent = parent

        # background
        background = wx.StaticBitmap(self)
        background.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/Select_Recipe.png"))

        # Text (picture)
        title = wx.StaticBitmap(background, pos=(130, 20))
        title.SetBitmap(wx.Bitmap(curWorkDir + "/pictures/Recipe_Selection_Title.png"))

        self.font1 = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        # File browser
        self.fbb = wx.lib.filebrowsebutton.FileBrowseButton(background,
                                                            labelText="Select a recipe:", fileMask="*.txt",
                                                            toolTip="Type recipe name or click browse to choose a recipe",
                                                            dialogTitle="Choose a recipe",
                                                            startDirectory=curWorkDir + "/Recipes_List", initialValue="",
                                                            changeCallback=self.ShowBtnConfirm)
        # setup the layout with sizers
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.fbb, 1, wx.ALIGN_CENTER_VERTICAL)

        # create a border space
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(hsizer, 100, wx.EXPAND | wx.ALL, 15)
        background.SetSizer(border)

        # Button
        self.confirmBtn = wx.Button(background, label="Confirm selection", pos=(370, 190), size=(200, 50))
        self.confirmBtn.SetFont(self.font1)
        self.confirmBtn.Hide()

        # Button event
        self.confirmBtn.Bind(wx.EVT_BUTTON, self.ConfirmSelection)

        self.Center()
        self.Show()

    def ShowBtnConfirm(self, event):
        global currentRecipe
        curWorkDirOriginal = curWorkDir.replace("/", "\\")              # The file browser gets the path with "\"...
        RecipeListDir = curWorkDirOriginal + "\\Recipes_List\\"         # Directory of Recipe List in Windows's explorer
        SelectedRecipePath = self.fbb.GetValue()                        # Value of the TextControl in the FileBrowser
        print("SelectedRecipePath: ", SelectedRecipePath)               # print the path of the selected recipe
        currentRecipe = SelectedRecipePath.replace(RecipeListDir, "")  # we only keep the name of the recipe
        print("SelectedRecipe: ", currentRecipe)
        self.confirmBtn.Show()                                          # The "Confirm" button appears

    def ConfirmSelection(self, event):

        global DrinkOrderDisplay
        global currentRecipe
        with open(RecipeListDir + currentRecipe, 'r') as f:  # we creat a list of the words in the selected recipe
            ListOfWords = [word for line in f for word in line.split()]

        print(ListOfWords)
        # We search for ingredients and quantities in the selected recipe and we display them via "DrinkOrderDisplay"
        # remember that DrinkOrderDisplay is used for the OrderDisplay value in the OrderADrinkFrame
        for ii in range(len(ListOfWords)):
            if ListOfWords[ii] == "INGREDIENT_1" \
                    or ListOfWords[ii] == "INGREDIENT_2" \
                    or ListOfWords[ii] == "INGREDIENT_3":
                DrinkOrderDisplay = "   "+DrinkOrderDisplay+ListOfWords[ii]+"\t\t\t"+ListOfWords[ii+3]+"\n"+"        "

        self.parent.UpdateOrderDisplay()  # We update the TextCtrl in the OrderADrinkFrame window

        self.Close()

mainWindow = MainWindow(None)
app.MainLoop()
