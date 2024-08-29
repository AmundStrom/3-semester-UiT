from cpuElement import CPUElement

class Control(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputoutputControlSignals):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputoutputControlSignals)
        
        assert(len(inputSources) == 1), 'Control should have one input'
        assert(len(outputValueNames) == 0), 'Control has no output'
        assert(len(control) == 0), 'Control has no control input'
        assert(len(outputoutputControlSignals) == 10), 'Control should have ten control output'
        
        # Opcode Input
        self.inputName = inputSources[0][1]

        # Control Outputs
        self.regDst = outputoutputControlSignals[0]
        self.aluSrc = outputoutputControlSignals[1]
        self.memToReg = outputoutputControlSignals[2]
        self.regWrite = outputoutputControlSignals[3]
        self.memRead = outputoutputControlSignals[4]
        self.memWrite = outputoutputControlSignals[5]
        self.branch = outputoutputControlSignals[6]
        self.aluOp = outputoutputControlSignals[7]
        self.jump = outputoutputControlSignals[8]
        self.lui = outputoutputControlSignals[9]

    def setControlSignals(self):
        assert(isinstance(self.inputValues[self.inputName], int))

        # Set all output control signals to zero.
        for signalName in self.outputControlSignals:
            self.outputControlSignals[signalName] = 0

        # Check what output control signals to be activated by fetching the input given from instruction[31:26]
        if self.inputValues[self.inputName] == 0:
            print("control.py: R-format")
            self.outputControlSignals[self.regDst] = 1
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.aluOp] = 2

        elif self.inputValues[self.inputName] == 2:
            print("control.py: j")
            self.outputControlSignals[self.jump] = 1
            self.outputControlSignals[self.aluOp] = 1

        elif self.inputValues[self.inputName] == 4:
            print("control.py: beq")
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.aluOp] = 1

        elif self.inputValues[self.inputName] == 5:
            print("control.py: bne")
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.aluOp] = 3 # only used on "bne"

        elif self.inputValues[self.inputName] == 8:
            print("control.py: addi")
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.regWrite] = 1

        elif self.inputValues[self.inputName] == 9:
            print("control.py: addiu")
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.regWrite] = 1

        elif self.inputValues[self.inputName] == 15:
            print("control.py: lui")
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.lui] = 1 # Special signal that is only used for "lui"

        elif self.inputValues[self.inputName] == 35:
            print("control.py: lw")
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memToReg] = 1
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 1

        elif self.inputValues[self.inputName] == 43:
            print("control.py: sw")
            self.outputControlSignals[self.aluSrc] = 1
            self.outputControlSignals[self.memWrite] = 1

    def writeOutput(self):
        pass
        