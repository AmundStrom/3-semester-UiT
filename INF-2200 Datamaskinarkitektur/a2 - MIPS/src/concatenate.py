from cpuElement import CPUElement

class Concatenate(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Concatenate should have two inputs'
        assert(len(outputValueNames) == 1), 'Concatenate has only one output'
        assert(len(control) == 0), 'Concatenate should not have any control signal'
        assert(len(outputSignalNames) == 0), 'Concatenate should not have any control output'
        
        # Inputs
        self.inputZero = inputSources[0][1] # Input zero should be bits [27-0]
        self.inputOne = inputSources[1][1] # Input one should be bits [31-28]

        # Outputs
        self.outputName = outputValueNames[0]
    
    def writeOutput(self):
        assert(isinstance(self.inputValues[self.inputZero], int))
        assert(isinstance(self.inputValues[self.inputOne], int))

        # convert to binary
        inputZero = bin(self.inputValues[self.inputZero])[2:].zfill(32)
        inputOne = bin(self.inputValues[self.inputOne])[2:].zfill(32)

        # split binary strings
        zeroSplit = inputZero[5:32]
        oneSplit = inputOne[0:5]

        concatenate = oneSplit + zeroSplit
        
        self.outputValues[self.outputName] = int(concatenate, 2) # Convert to integer
        
        print("concatenate.py: Output Jump address: ", self.outputValues[self.outputName])