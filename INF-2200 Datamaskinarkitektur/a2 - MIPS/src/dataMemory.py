'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
        
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Datamemory should have two inputs'
        assert(len(outputValueNames) == 1), 'Datamemory has only one output'
        assert(len(control) == 2), 'Datamemory has two control signal'
        assert(len(outputSignalNames) == 0), 'Datamemory should not have any control output'
        
        # Inputs
        self.address = inputSources[0][1]
        self.writeData = inputSources[1][1]

        # Outputs
        self.outputName = outputValueNames[0]

        # Control inputs
        self.memWrite = control[0][1]
        self.memRead = control[1][1]
    
    def writeOutput(self):
        self.outputValues[self.outputName] = 0
        # Check what operation should be preformed by fetching the control signals

        # Store word
        if(self.controlSignals[self.memWrite] == 1):
            print("dataMemory.py: Store")
            self.memory[self.inputValues[self.address]] = self.inputValues[self.writeData]
            print("dataMemory.py: address: ", self.memory[self.inputValues[self.address]], " input: ", self.inputValues[self.writeData])
            
        # Load word
        if(self.controlSignals[self.memRead] == 1):
            print("dataMemory.py: Load")
            readData = self.memory[self.inputValues[self.address]]
            self.outputValues[self.outputName] = readData
