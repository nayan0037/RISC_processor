from instruction import *
from branchPred import *
class decode_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        instr = instruction_class()
        instr.PC = self.instr.PC
        # print(type(instr))
        instr.decode(self.instr)
        self.instr=instr
        # self.instr.PC = self.processor.programCounter - 4 
        if(self.instr.is_branch):
            (BTA, pred) = self.processor.branch_pred.predict(self.instr.PC)
            if pred == "1": 
                self.processor.programCounter = BTA
                self.processor.BTA_hist.append(BTA) 
            self.processor.branch_hist.append(pred)
            self.instr.opr2Value = self.instr.immediate
            self.processor.speculative = True
