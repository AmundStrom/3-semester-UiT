'''
Code written for inf-2200, University of Tromso
'''

import unittest
from testElement import TestElement
from cpuElement import CPUElement
import common


class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}
        # Note that we won't actually use all the registers listed here...
        self.registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                              '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                              '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                              '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 4), 'Register file should have four inputs'
        assert(len(outputValueNames) == 2), 'Register file should have two outputs'
        assert(len(control) == 1), 'Register file should have one control signal'
        assert(len(outputSignalNames) == 0), 'Register file should not have any control output'

        # Inputs
        self.readReg1 = inputSources[0][1]      # Instruction [25:21]
        self.readReg2 = inputSources[1][1]      # Instruction [20:16] or ignore
        self.writeReg = inputSources[2][1]      # Instruction [20:16] or [15:11] 
        self.writeData = inputSources[3][1]     # Write data after R-type or Load

        # Outputs
        self.readData1 = outputValueNames[0]
        self.readData2 = outputValueNames[1]

        # Control input
        self.RegWrite = control[0][1]

    def writeOutput(self):
        
        # Outputs are the value the given registers hold
        register = self.inputValues[self.readReg1] # Get registers which are to be read
        assert(isinstance(register, int))
        self.outputValues[self.readData1] = self.register[register] # Get value which the given register holds, and set as output

        register = self.inputValues[self.readReg2]
        assert(isinstance(register, int))
        self.outputValues[self.readData2] = self.register[register]

    def setRegData(self):
        '''
        Write data given from data memory or ALU into the writeReg.
        This is executed at the end of a cycle.
        '''

        if(self.controlSignals[self.RegWrite] == 1):
            self.readInput()

            register = self.inputValues[self.writeReg] # Get register to write into
            assert(isinstance(register, int))
            data = self.inputValues[self.writeData] # Get data which is to be written
            assert(isinstance(data, int))
            
            self.register[register] = data
            print("registerFile.py: Write this value: ", self.inputValues[self.writeData], " into this register: ", self.registerNames[self.inputValues[self.writeReg]])

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (self.registerNames[i], common.fromUnsignedWordToSignedWord(
                self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()


class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.registerFile = RegisterFile()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['readReg1', 'readReg2', 'writeReg', 'writeData'],
            [],
            ['regWrite']
        )

        self.registerFile.connect(
            [(self.testInput, 'readReg1'), (self.testInput, 'readReg2'), (self.testInput, 'writeReg'), (self.testInput, 'writeData')],
            ['readData1', 'readData2'],
            [(self.testInput, 'regWrite')],
            []
        )

        self.testOutput.connect(
            [(self.registerFile, 'readData1'), (self.registerFile, 'readData2')],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        # First cycle
        self.testInput.setOutputValue('readReg1', 10)
        self.testInput.setOutputValue('readReg2', 9)
        self.testInput.setOutputValue('writeReg', 10)
        self.testInput.setOutputControl('regWrite', 1)

        self.registerFile.readControlSignals()
        self.registerFile.readInput()
        self.registerFile.writeOutput()
        self.registerFile.setControlSignals()

        self.testInput.setOutputValue('writeData', 2782)
        self.registerFile.setRegData()

        # Second cycle
        self.testInput.setOutputValue('readReg1', 10)
        self.testInput.setOutputValue('readReg2', 8)
        self.testInput.setOutputValue('writeReg', 7)
        self.testInput.setOutputControl('regWrite', 1)

        self.registerFile.readControlSignals()
        self.registerFile.readInput()
        self.registerFile.writeOutput()
        self.registerFile.setControlSignals()

        self.testOutput.readInput()
        output1 = self.testOutput.inputValues['readData1']
        output2 = self.testOutput.inputValues['readData2']
        self.assertEqual(output1, 2782)
        self.assertEqual(output2, 0)

        self.testInput.setOutputValue('writeData', 1691)
        self.registerFile.setRegData()

        self.registerFile.printAll()

if __name__ == '__main__':
    unittest.main()
