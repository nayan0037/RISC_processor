class operandRead_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        if (self.instr.regRead):
            if not self.instr.operand1 in self.processor.hazardList:
                self.instr.opr1Value = self.processor.registers[self.instr.operand1]
            else: 
                if self.instr.operand1 == self.processor.pipeline[3].instr.dest and not self.processor.pipeline[3].instr.is_load:
                    self.instr.forwardEE_opr1 = True
                elif self.instr.operand1 == self.processor.pipeline[4].instr.dest and self.processor.pipeline[4].instr.is_load:
                    self.instr.forwardME_opr1 = True                
                else:
                    self.processor.nstall = True
            if (self.instr.is_branch or self.instr.opcode == "sw" or self.instr.type == "rtype"):
                    if not self.instr.operand2 in self.processor.hazardList:
                        self.instr.opr2Value = self.processor.registers[self.instr.operand2]
                    else:
                        if self.instr.operand2 == self.processor.pipeline[3].instr.dest and not self.processor.pipeline[3].instr.is_load:
                            self.instr.forwardEE_opr2 = True
                        elif self.instr.operand2 == self.processor.pipeline[4].instr.dest and self.processor.pipeline[4].instr.is_load:
                            self.instr.forwardME_opr2 = True                                   
                        else:
                            self.processor.nstall = True
    
        ######## handle jump here
