'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from signExtend import SignExtend
from upperExtend import UpperExtend
from shiftLeftTwo import ShiftLeftTwo
from control import Control
from aluControl import ALUControl
from alu import ALU
from andOP import AND
from concatenate import Concatenate


class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''

    def __init__(self, memoryFile):
        self.nCycles = 0  # Used to hold number of clock cycles spent executing instructions

        self.dataMemory = DataMemory(memoryFile) # Step Memory access
        self.instructionMemory = InstructionMemory(memoryFile) # Step Instruction Fetch

        # Step Instruction Fetch
        self.pc = PC(self.startAddress())
        self.constant4 = Constant(4)
        self.adderLeft = Add()

        # Step Instruction Decode/register file read
        self.shiftLeftUpper = ShiftLeftTwo()
        self.concatenate = Concatenate() # Added element to make jump possible
        self.control = Control()
        self.muxToRegOne = Mux()
        self.registerFile = RegisterFile()
        self.signExtend = SignExtend()
        self.upperExtend = UpperExtend() # Added element to make operation "lui" possible

        # Step Execute/address calculation
        self.shiftLeftLower = ShiftLeftTwo()
        self.adderRight = Add()
        self.muxToALU = Mux()
        self.aluControl = ALUControl()
        self.alu = ALU()

        # Step Memory access
        self.andOP = AND()
        self.muxToMuxToPC = Mux()
        self.muxToPC = Mux() # Step Write back
        self.muxToMuxToWriteData = Mux()
        self.muxToWriteData = Mux() # Step Write back, also added mux to make operation "lui" possible
        
        # divided into steps
        self.elements = [self.pc, self.constant4, self.adderLeft, self.instructionMemory,
                         self.shiftLeftUpper, self.concatenate, self.control, self.muxToRegOne, self.registerFile, self.signExtend, self.upperExtend,
                         self.shiftLeftLower, self.adderRight, self.muxToALU, self.aluControl, self.alu,
                         self.andOP, self.muxToMuxToPC, self.muxToPC, self.dataMemory, self.muxToMuxToWriteData, self.muxToWriteData]

        self._connectCPUElements()

    def _connectCPUElements(self):

        self.pc.connect(
            [(self.muxToPC, 'nextAddress')],
            ['pcAddress'],
            [],
            []
        )

        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.adderLeft.connect(
            [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
            ['sumLeft'],
            [],
            []
        )

        self.instructionMemory.connect(
            [(self.pc, 'pcAddress')],
            ['opcode', 'rs', 'rt', 'rd', 'funct', 'address16', 'address26'],
            [],
            []
        )

        self.shiftLeftUpper.connect(
            [(self.instructionMemory, 'address26')],
            ['address28'],
            [],
            []
        )

        self.concatenate.connect(
            [(self.shiftLeftUpper, 'address28'), (self.adderLeft, 'sumLeft')],
            ['jumpAddress'],
            [],
            []
        )

        self.control.connect(
            [(self.instructionMemory, 'opcode')],
            [],
            [],
            ['regDst', 'aluSrc', 'memToReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump', 'lui']
        )

        self.muxToRegOne.connect(
            [(self.instructionMemory, 'rt'), (self.instructionMemory, 'rd')],
            ['writeReg'],
            [(self.control, 'regDst')],
            []
        )

        self.registerFile.connect(
            [(self.instructionMemory, 'rs'), (self.instructionMemory, 'rt'), 
             (self.muxToRegOne, 'writeReg'), (self.muxToWriteData, 'writeData')],
            ['readData1', 'readData2'],
            [(self.control, 'regWrite')],
            []
        )

        self.signExtend.connect(
            [(self.instructionMemory, 'address16')],
            ['signExtend'],
            [],
            []
        )

        self.upperExtend.connect(
            [(self.instructionMemory, 'address16')],
            ['upperExtend'],
            [],
            []
        )

        self.shiftLeftLower.connect(
            [(self.signExtend, 'signExtend')],
            ['signExtendShift'],
            [],
            []
        )

        self.adderRight.connect(
            [(self.adderLeft, 'sumLeft'), (self.shiftLeftLower, 'signExtendShift')],
            ['sumRight'],
            [],
            []
        )

        self.muxToALU.connect(
            [(self.registerFile, 'readData2'), (self.signExtend, 'signExtend')],
            ['ALUinput2'],
            [(self.control, 'aluSrc')],
            []
        )

        self.aluControl.connect(
            [(self.instructionMemory, 'funct')],
            [],
            [(self.control, 'aluOp')],
            ['aluOpOut']
        )

        self.alu.connect(
            [(self.registerFile, 'readData1'), (self.muxToALU, 'ALUinput2')],
            ['ALUresult'],
            [(self.aluControl, 'aluOpOut')],
            ['zero']
        )

        self.andOP.connect(
            [],
            [],
            [(self.control, 'branch'), (self.alu, 'zero')],
            ['andOP']
        )

        self.muxToMuxToPC.connect(
            [(self.adderLeft, 'sumLeft'), (self.adderRight, 'sumRight')],
            ['incrementOrBranch'],
            [(self.andOP, 'andOP')],
            []
        )

        self.muxToPC.connect(
            [(self.muxToMuxToPC, 'incrementOrBranch'), (self.concatenate, 'jumpAddress')],
            ['nextAddress'],
            [(self.control, 'jump')],
            []
        )

        self.dataMemory.connect(
            [(self.alu, 'ALUresult'), (self.registerFile, 'readData2')],
            ['readData'],
            [(self.control, 'memWrite'), (self.control, 'memRead')],
            []
        )

        self.muxToMuxToWriteData.connect(
            [(self.alu, 'ALUresult'), (self.dataMemory, 'readData')],
            ['memoryOrALU'],
            [(self.control, 'memToReg')],
            []
        )
        
        self.muxToWriteData.connect(
            [(self.muxToMuxToWriteData, 'memoryOrALU'), (self.upperExtend, 'upperExtend')],
            ['writeData'],
            [(self.control, 'lui')],
            []
        )

    def startAddress(self):
        '''
        Returns first instruction from instruction memory
        '''
        return next(iter(sorted(self.instructionMemory.memory.keys())))

    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def breakInstruction(self):
        '''Return True if a break instruction is to be executed, otherwise False.'''
        if(self.instructionMemory.breakIns == True):
            return True
        else:
            return False

    # def dataMemory(self):
    #     '''Returns dictionary, mapping memory addresses to data, holding
    #     data memory after instructions have finished executing.'''

    #     return self.dataMemory.memory

    # def registerFile(self):
    #     '''Returns dictionary, mapping register numbers to data, holding
    #     register file after instructions have finished executing.'''

    #     return self.registerFile.register

    # def printDataMemory(self):
    #     self.dataMemory.printAll()

    # def printRegisterFile(self):
    #     self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''
        self.nCycles += 1

        print()
        print()
        print("Cycles: ", self.nCycles)
        print()

        # The following is just a small sample implementation

        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
        self.registerFile.setRegData() # Step Write back

        print(self.registerFile.register)