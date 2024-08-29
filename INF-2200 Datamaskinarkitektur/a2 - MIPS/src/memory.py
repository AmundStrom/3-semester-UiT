'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import common

class Memory(CPUElement):
    def __init__(self, filename):
    
        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'long'
        self.memory = {}
        self.breakRead = 3 # Used for testfiles, "test" + 1
        
        self.initializeMemory(filename)
    
    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''
        counter = 0
        # Open and read file
        with open(filename, "r") as infile:
            content = infile.readlines()
            for i in content:
                # This check is used for test files
                if(i[0] == ">"):
                    counter = counter + 1
                    if(self.breakRead == counter):
                        break
                # Split line, convert to integer, and put in memory
                if( (i[0] != "#") and (i != "\n") and (i[0] != ">") ):
                    l = i.split("\t")
                    hex_mem = l[0]
                    hex_ins = l[1]

                    bin_mem = int(hex_mem, 16)
                    bin_ins = int(hex_ins, 16)

                    self.memory[bin_mem] = bin_ins
        print()
        print()

    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))
