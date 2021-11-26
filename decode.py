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

        # if self.instr.operand1 in self.processor.hazardList:
        #     # print("toh act bsdk")
        #     self.processor.stall = True
        # if self.instr.operand2 in self.processor.hazardList:
        #     self.processor.stall = True

        if(self.instr.is_branch):
            self.instr.opr2Value = self.instr.immediate
        if self.instr.regWrite:
            if(self.instr.dest != "$r0" and (not self.processor.stall)):
                self.processor.hazardList.append(self.instr.dest)
                if self.instr.opcode != "lw":
                    self.processor.hazardType.append("Execute")
                else:
                    self.processor.hazardType.append("Memory")
