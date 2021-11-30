from instruction import *

class fetch_stage(object):
    """docstring for fetch_stage"""
    def __init__(self, instruction,processor):
        self.instr = instruction
        self.processor = processor

    def advance(self):
        if not self.processor.stall:
            instr1 = self.processor.prog_memory[self.processor.programCounter]
            if(not self.processor.stall and instr1 != "nop"):
                self.processor.instrCount += 1
            
            self.instr.instruction = instr1
            self.instr.PC = self.processor.programCounter
            self.instr.decode_opcode(self.instr)
            if(self.instr.is_branch):
                (BTA, pred) = self.processor.branch_pred.predict(self.processor.programCounter)
                if pred == "1": 
                    self.processor.programCounter = BTA
                    self.processor.BTA_hist.append(BTA) 
                else:
                    self.processor.programCounter += 4
                self.processor.branch_hist.append(pred)
                self.instr.opr2Value = self.instr.immediate
                self.processor.speculative = True
        
            elif(self.instr.is_jump):
                if(self.processor.speculative) :
                    self.processor.bstall = True
                else:    
                    BTA = self.instr.BTA
                    self.processor.programCounter = int(BTA)
            else:
                self.processor.programCounter += 4

