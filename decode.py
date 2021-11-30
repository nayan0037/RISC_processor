from instruction import *
from branchPred import *
from fetch import *

class decode_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        self.instr.decode()
