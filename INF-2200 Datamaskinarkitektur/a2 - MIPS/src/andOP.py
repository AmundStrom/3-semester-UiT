from cpuElement import CPUElement

class AND(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 0), 'And should not have any inputs'
        assert(len(outputValueNames) == 0), 'Andr should not have any outputs'
        assert(len(control) == 2), 'And has two control signals'
        assert(len(outputSignalNames) == 1), 'And should have one control output'
        
        # Control inputs
        self.controlZero = control[0][1]
        self.controlOne = control[1][1]

        # Control output
        self.outputName = outputSignalNames[0]

    def setControlSignals(self):
        # Fetch inputs
        zero = self.controlSignals[self.controlZero]
        assert(isinstance(zero, int))

        one = self.controlSignals[self.controlOne]
        assert(isinstance(one, int))

        self.outputControlSignals[self.outputName] = zero and one
  
    def writeOutput(self):
        pass
