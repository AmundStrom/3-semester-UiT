from cpuElement import CPUElement

class ALUControl(CPUElement):

	def connect(self, inputSources, outputValueNames, control, outputSignalNames):
		CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

		assert(len(inputSources) == 1), 'ALU Control has only one inputs'
		assert(len(outputValueNames) == 0), 'ALU Control should not have any outputs'
		assert(len(control) == 1), 'ALU has only one control signal'
		assert(len(outputSignalNames) == 1), 'ALU has only one control output'
		
		# Input
		self.inputName = inputSources[0][1]
	
		# Control input
		self.conInput = control[0][1]

		# Control Output
		self.conOutput = outputSignalNames[0]

	def setControlSignals(self):
		assert(isinstance(self.inputValues[self.inputName], int))
		assert(isinstance(self.controlSignals[self.conInput], int))
		
		# Determine what operation the ALU element should preferm.
		# First checks use the control signal fetched from the control unit.
		if(self.controlSignals[self.conInput] == 0):
			print("aluControl.py: Load word/Store word, add")
			self.outputControlSignals[self.conOutput] = 2
			return

		elif(self.controlSignals[self.conInput] == 1):
			print("aluControl.py: Branch, sub")
			self.outputControlSignals[self.conOutput] = 6
			return

		elif(self.controlSignals[self.conInput] == 2):
			# Second checks use the input fetched from the instruction[0:5].
			if(self.inputValues[self.inputName] == 32):
				print("aluControl.py: R-type, add")
				self.outputControlSignals[self.conOutput] = 2
				return

			if(self.inputValues[self.inputName] == 34):
				print("aluControl.py: R-type, sub")
				self.outputControlSignals[self.conOutput] = 6
				return

			if(self.inputValues[self.inputName] == 36):
				print("aluControl.py: R-type, AND")
				self.outputControlSignals[self.conOutput] = 0
				return

			if(self.inputValues[self.inputName] == 37):
				print("aluControl.py: R-type, OR")
				self.outputControlSignals[self.conOutput] = 1
				return

			if(self.inputValues[self.inputName] == 42):
				print("aluControl.py: R-type, set on less than")
				self.outputControlSignals[self.conOutput] = 7
				return

		# Unique self defined check, not included in the textbook
		elif(self.controlSignals[self.conInput] == 3):
			print("aluControl.py: bne")
			self.outputControlSignals[self.conOutput] = 8 
			return

		assert("aluControl.py, Did not set control signal")

	def writeOutput(self):
		pass
