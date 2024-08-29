from cpuElement import CPUElement

class ALU(CPUElement):
    def __init__(self):
        self.branch = False # Used for branch operations

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'ALU should have two inputs'
        assert(len(outputValueNames) == 1), 'ALU has only one output'
        assert(len(control) == 1), 'ALU has only one control signal'
        assert(len(outputSignalNames) == 1), 'ALU has only one control output'
        
        # Inputs
        self.inputRead = inputSources[0][1]
        self.inputMux = inputSources[1][1]

        # Outputs
        self.outputName = outputValueNames[0]
        self.conOutput = outputSignalNames[0]

        # Control input
        self.conInput = control[0][1]
    
    def writeOutput(self):
        assert(isinstance(self.inputValues[self.inputRead], int))
        assert(isinstance(self.inputValues[self.inputMux], int))
        assert(isinstance(self.controlSignals[self.conInput], int))

        print("alu.py: input 0: ", self.inputValues[self.inputRead])
        print("alu.py: input 1: ", self.inputValues[self.inputMux])

        # Fetch and convert inputs using 2'complement into integers
        read = self.twos_comp(self.inputValues[self.inputRead], 32)
        mux = self.twos_comp(self.inputValues[self.inputMux], 32)
        
        # Check what kind of operation to preform by fetching the control signal input
        # Every result is 'masked' which ignores overflow
        if(self.controlSignals[self.conInput] == 2):
            print("alu.py: add")
            result = read + mux
            self.outputValues[self.outputName] = result & 0xffffffff
            print("alu.py: result: ", self.outputValues[self.outputName])
            return
            
        elif(self.controlSignals[self.conInput] == 6):
            print("alu.py: sub and beq")
            result = read - mux
            self.outputValues[self.outputName] = result & 0xffffffff

            if(self.outputValues[self.outputName] == 0):
                self.branch = True

            print("alu.py: result: ", self.outputValues[self.outputName])
            return

        elif(self.controlSignals[self.conInput] == 8):
            print("alu.py: sub and bne")
            result = read - mux
            self.outputValues[self.outputName] = result & 0xffffffff
            
            if(self.outputValues[self.outputName] != 0):
                self.branch = True
            
            print("alu.py: result: ", self.outputValues[self.outputName])
            return

        elif(self.controlSignals[self.conInput] == 0):
            print("alu.py: AND")
            result = read & mux
            self.outputValues[self.outputName] = result & 0xffffffff
            print("alu.py: result: ", self.outputValues[self.outputName])
            return

        elif(self.controlSignals[self.conInput] == 1):
            print("alu.py: OR")
            result = read | mux
            self.outputValues[self.outputName] = result & 0xffffffff
            print("alu.py: result: ", self.outputValues[self.outputName])
            return
            
        elif(self.controlSignals[self.conInput] == 7):
            print("alu.py: set on less than")
            result = read - mux
            if result < 0:
                self.outputValues[self.outputName] = 1
                print("alu.py: result: ", self.outputValues[self.outputName])
                return
            if result >= 0:
                self.outputValues[self.outputName] = 0
                print("alu.py: result: ", self.outputValues[self.outputName])
                return
            assert("alu.py: Did not carry out 'set on less than'")
            
        assert("alu.py, Did not set output value")

    def setControlSignals(self):
        self.outputControlSignals[self.conOutput] = 0

        # Used if branch
        if(self.branch == True):
            print("alu.py: Branch is True")
            self.outputControlSignals[self.conOutput] = 1
            self.branch = False

    def twos_comp(self, val, bits):
        '''
        compute the 2's complement of int value val
        
        Source: https://stackoverflow.com/questions/1604464/twos-complement-in-python
        '''
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is