from cpuElement import CPUElement

class ShiftLeftTwo(CPUElement):
    def __init__(self):
        self.shift = '00'

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Shift left has only one inputs'
        assert(len(outputValueNames) == 1), 'Shift left has only one output'
        assert(len(control) == 0), 'Shift left hould not have any control signal'
        assert(len(outputSignalNames) == 0), 'Shift left should not have any control output'
        
        # Input
        self.inputName = inputSources[0][1]

        # Output
        self.outputName = outputValueNames[0]
    
    def writeOutput(self):
        assert(isinstance(self.inputValues[self.inputName], int))

        input = bin(self.inputValues[self.inputName])[2:].zfill(32) # Get input and convert to binary
        # Remove first two characters of input, add two zeros to the right of the body, convert to integer
        self.outputValues[self.outputName] = int(input[2:] + self.shift, 2)

        print("shiftLeftTwo.py: BINARY input: ", input, " Output: ", bin(self.outputValues[self.outputName])[2:])
        print("shiftLeftTwo.py: INTEGER input: ", self.inputValues[self.inputName], " Output: ", (self.outputValues[self.outputName]))