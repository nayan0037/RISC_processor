from instruction import *

class fetch_stage(object):
    """docstring for fetch_stage"""
    def __init__(self, instruction,processor):
        self.instr = instruction
        self.processor = processor

    def advance(self):
        instr1 = self.processor.prog_memory[self.processor.programCounter]
        self.instr=instruction_class()
        self.instr.instruction = instr1
        self.processor.programCounter += 4
