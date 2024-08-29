from cpuElement import CPUElement

class SignExtend(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Sign extend has only one inputs'
        assert(len(outputValueNames) == 1), 'Sign extend has only one output'
        assert(len(control) == 0), 'Sign extend hould not have any control signal'
        assert(len(outputSignalNames) == 0), 'Sign extend should not have any control output'
        
        # Input
        self.inputName = inputSources[0][1]

        # Output
        self.outputName = outputValueNames[0]
    
    def writeOutput(self):
        assert(isinstance(self.inputValues[self.inputName], int))

        input = bin(self.inputValues[self.inputName])[2:].zfill(16) # Get input and convert to binary
        leftMostBit = input[0]
        
        extended = ''
        for _ in range(16):
            extended = leftMostBit + extended

        output = extended + input
        self.outputValues[self.outputName] = int(output, 2)
        
        print("signextend.py: BINARY input: ", input, " Output: ", bin(self.outputValues[self.outputName])[2:])
        print("signextend.py: INTEGER input: ", self.inputValues[self.inputName], " Output: ", (self.outputValues[self.outputName]))