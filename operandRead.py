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
                self.processor.nstall = True
            if (self.instr.is_branch or self.instr.opcode == "sw" or self.instr.type == "rtype"):
                    if not self.instr.operand2 in self.processor.hazardList:
                        self.instr.opr2Value = self.processor.registers[self.instr.operand2]
                    else:
                        self.processor.nstall = True

        ######## handle jump here
