from instruction import *
from branchPred import *
from fetch import *

class decode_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        instr = instruction_class()
        instr.PC = self.instr.PC
        instr.decode(self.instr)
        self.instr=instr
        if(self.instr.is_branch):
            (BTA, pred) = self.processor.branch_pred.predict(self.instr.PC)
            if pred == "1": 
                self.processor.programCounter = BTA
                self.processor.BTA_hist.append(BTA) 
            self.processor.branch_hist.append(pred)
            self.instr.opr2Value = self.instr.immediate
            self.processor.speculative = True
        if(self.instr.is_jump):
            if(self.processor.speculative):
                self.processor.bstall = True
            else:    
                BTA = self.instr.BTA
                self.processor.programCounter = int(BTA)
                self.processor.pipeline[0] = fetch_stage(instruction_class(),self)