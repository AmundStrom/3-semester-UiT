'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory

class InstructionMemory(Memory):
	def __init__(self, filename):
		Memory.__init__(self, filename)
		self.breakIns = False
	
	def connect(self, inputSources, outputValueNames, control, outputSignalNames):
		CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

		assert(len(inputSources) == 1), 'Instruction Memory should have one inputs'
		assert(len(outputValueNames) == 7), 'Instruction Memory has seven outputs, since input is split into six different instructions'
		assert(len(control) == 0), 'Instruction Memory should not have any control signal'
		assert(len(outputSignalNames) == 0), 'Instruction Memory should not have any control output'

		# Input
		self.address = inputSources[0][1]

		# Value of each output
		# ____________________________________________________________________________________
		# |         |   Source      |   Source/     |   Destimation |   Shift    |   Function|
		# | Opcode  |   Register    |   Destination |   Register    |   Amount   |   Code    |
		# |         |   (rs)        |   Register(rt)|   (rd)        |   (shamt)  |   (funct) |
		# ————————————————————————————————————————————————————————————————————————————————————
		#   31:26       25:21           20:16           15:11           10:6        5:0
		#           __________________________________________________________________________
		#           |                               |                                        |
		#           |   Address(jump)               |   Address(Lw/Sw, Br)                   |
		#           |                               |                                        |
		#           ——————————————————————————————————————————————————————————————————————————
		#               25:0                            15:0
		self.opcode = outputValueNames[0]
		self.rs = outputValueNames[1]
		self.rt = outputValueNames[2]
		self.rd = outputValueNames[3]
		self.funct = outputValueNames[4]
		self.address16 = outputValueNames[5]
		self.address26 = outputValueNames[6]
	
	def writeOutput(self):

		memory = self.inputValues[self.address] # Get memory address for the instruction
		assert(isinstance(memory, int))

		dec_ins = self.memory[memory] # Get instruction from memory
		assert(isinstance(dec_ins, int))

		bin_ins = bin(dec_ins)[2:].zfill(32) # Convert instruction to binary

		# Slice up instructions
		self.outputValues[self.opcode] = int(bin_ins[0:6],2)
		self.outputValues[self.rs] = int(bin_ins[6:11],2)
		self.outputValues[self.rt] = int(bin_ins[11:16],2)
		self.outputValues[self.rd] = int(bin_ins[16:21],2)
		self.outputValues[self.funct] = int(bin_ins[26:32],2)
		self.outputValues[self.address16] = int(bin_ins[16:32],2)
		self.outputValues[self.address26] = int(bin_ins[6:32],2)
		
		# Check if it is a break instruction
		if(dec_ins == 13):
			self.breakIns = True

		print("instruction[31-26] opcode: ", self.outputValues[self.opcode])
		print("instruction[25-21] rs: ", self.outputValues[self.rs])
		print("instruction[20-16] rt: ", self.outputValues[self.rt])
		print("instruction[15-11] rd: ", self.outputValues[self.rd])
		print("instruction[5-0] funct: ", self.outputValues[self.funct])
		print("instruction[15-0] address16: ", self.outputValues[self.address16])
		print("instruction[25-0] address26: ", self.outputValues[self.address26])