from instruction import *

class decode_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        instr = instruction_class()
        # print(type(instr))
        instr.decode(self.instr)
        self.instr=instr

        if(self.instr.is_branch):
            self.instr.opr2Value = self.instr.immediate
        if self.instr.regWrite:
            if(self.instr.dest != "$r0" and (not self.processor.stall)):
                self.processor.hazardList.append(self.instr.dest)
                if self.instr.is_load:
                    self.processor.hazardType.append("Memory")
                else:
                    self.processor.hazardType.append("Execute")
