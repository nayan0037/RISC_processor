class operandRead_stage():
    """docstring for decode_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        if (self.instr.regRead):
            self.instr.opr1Value = self.processor.registers[self.instr.operand1]

            if (self.instr.is_branch or self.instr.opcode == "sw" or self.instr.type == "rtype"):
                self.instr.opr2Value = self.processor.registers[self.instr.operand2]

        opr1 = self.instr.operand1
        opr2 = self.instr.operand2
        is_loadO = self.instr.is_load
        destE = self.processor.pipeline[3].instr.dest
        is_loadE = self.processor.pipeline[3].instr.is_load
        destM = self.processor.pipeline[4].instr.dest
        is_loadM = self.processor.pipeline[4].instr.is_load
        destW = self.processor.pipeline[5].instr.dest
        is_loadW = self.processor.pipeline[5].instr.is_load

        if (self.instr.regRead):
            self.instr.forwardEE_opr1 = False       
            self.instr.forwardME_opr1 = False    
            if(opr1 == destE and not is_loadO and not is_loadE):
                self.instr.forwardEE_opr1 = True
            elif(opr1 == destM and not is_loadO and is_loadM):
                self.instr.forwardME_opr1 = True
            elif(opr1 == destM):
                ## E_E
                self.processor.nstall = True
            if(opr1 == destW):
                ## E__E
                self.processor.nstall = True
            if(opr1 == destE and is_loadE):
                ## ME
                self.processor.nstall = True
            

            if (self.instr.is_branch or self.instr.opcode == "sw" or self.instr.type == "rtype"):            
                self.instr.forwardEE_opr2 = False    
                self.instr.forwardME_opr2 = False    
                if(opr2 == destE and not is_loadO and not is_loadE):
                    self.instr.forwardEE_opr2 = True
                elif(opr2 == destM and not is_loadO and is_loadM):
                    self.instr.forwardME_opr2 = True
                elif(opr2 == destM):
                    ## E_E
                    self.processor.nstall = True
                if(opr2 == destW):
                    ## E__E
                    self.processor.nstall = True
                if(opr2 == destE and is_loadE):
                    ## ME
                    self.processor.nstall = True
     

