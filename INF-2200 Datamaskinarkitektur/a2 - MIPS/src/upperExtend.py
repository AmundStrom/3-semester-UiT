from cpuElement import CPUElement

class UpperExtend(CPUElement):
    '''
    This class is only used for the instruction "lui", and will extend the input by adding 16 bits of zero to the right of the body.
    The output of this element will go directly to the "write data" input of the registerfile.
    This means that there also has to be a new Mux that controls where the "write data" is coming from,
    which also means that there has to be an new control signal in the control unit called "lui".
    '''
    def __init__(self):
        self.extend = '0000000000000000'

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Upper extend has only one inputs'
        assert(len(outputValueNames) == 1), 'Upper extend has only one output'
        assert(len(control) == 0), 'Upper extend hould not have any control signal'
        assert(len(outputSignalNames) == 0), 'Upper extend should not have any control output'
        
        self.inputName = inputSources[0][1]
        self.outputName = outputValueNames[0]
    
    def writeOutput(self):
        assert(isinstance(self.inputValues[self.inputName], int))

        input = bin(self.inputValues[self.inputName])[2:] # Get input and convert to binary
        self.outputValues[self.outputName] = int(input + self.extend, 2) # Extend by adding zero to the right, and convert to integar
        
        print("upperExtend.py: BINARY input: ", input, " Output: ", bin(self.outputValues[self.outputName])[2:])
        print("upperExtend.py: INTEGER input: ", self.inputValues[self.inputName], " Output: ", (self.outputValues[self.outputName]))