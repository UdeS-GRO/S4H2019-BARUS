
import PositionFileManager
import unittest
import os
import SaveRecipe

workDirectory = os.getcwd() + "\\" + "PositionFileTest.txt"
dataWritten = []

def simulatedSend(data):
    # This function simulates a send via serial port
    global dataWritten
    dataWritten.append(data)

class AutomatedTests(unittest.TestCase):

# Position saving function and extraction test
    def test_save_positive_positions(self):
        posDict = {}
        PositionFileManager.saveNewPosition("HOME", 1000, 500, 1, posDict, workDirectory)
        savedPos = PositionFileManager.initPositionDictionary(workDirectory)
        # Checking motor 1 positive position save
        self.assertEqual(savedPos["HOME"][0], "1000")
        # Checking motor 2 positive position save
        self.assertEqual(savedPos["HOME"][1], "500")
        # Checking quantity position save
        self.assertEqual(savedPos["HOME"][2], "1")

    def test_save_negative_positions(self):
        posDict = {}
        PositionFileManager.saveNewPosition("HOME", -1000, -500, 0, posDict, workDirectory)
        savedPos = PositionFileManager.initPositionDictionary(workDirectory)
        # Checking motor 1 negative position save
        self.assertEqual(int(savedPos["HOME"][0]), -1000)
        # Checking motor 2 negative position save
        self.assertEqual(int(savedPos["HOME"][1]), -500)
        # Checking quantity position save
        self.assertEqual(int(savedPos["HOME"][2]), 0)

    def test_file_creation(self):
        # Create some test files
        SaveRecipe.CreateRecipe("test1")
        SaveRecipe.CreateRecipe("test2")
        SaveRecipe.CreateRecipe("test3")

        # Verifying if test files created exist
        result1 = os.path.isfile(os.getcwd()+"/"+"test1.txt")
        result2 = os.path.isfile(os.getcwd()+"/"+"test2.txt")
        result3 = os.path.isfile(os.getcwd()+"/"+"test3.txt")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)

    def test_serial_com(self):

        # Simulating a serial data write
        global dataWritten
        data1 = 5612
        data2 = -500
        data3 = 26

        simulatedSend(data1)
        simulatedSend(data2)
        simulatedSend(data3)

        self.assertEqual(dataWritten[0], 5612)
        self.assertEqual(dataWritten[1], -500)
        self.assertEqual(dataWritten[2], 26)





