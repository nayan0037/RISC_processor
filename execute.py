from instruction import *

class execute_stage():
    """docstring for execute_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        if self.instr.opcode != "nop" and self.instr.aluOp:
            if self.instr.forwardEE_opr1:
                self.instr.opr1Value = self.processor.pipeline[4].instr.result
            elif self.instr.forwardME_opr1:
                self.instr.opr1Value = self.processor.pipeline[5].instr.result
            if self.instr.forwardEE_opr2:
                self.instr.opr2Value = self.processor.pipeline[4].instr.result
            elif self.instr.forwardME_opr2:
                self.instr.opr2Value = self.processor.pipeline[5].instr.result


            if self.instr.opcode == "lw" or self.instr.opcode == "sw":
                self.instr.result = int(self.instr.opr1Value) + int(self.instr.immediate)
            elif self.instr.opcode == "bne":
                if self.instr.opr1Value != self.instr.opr2Value:
                    self.processor.programCounter += int(self.instr.immediate)*4 - 12
                    ## flush pipeline
                    self.processor.pipeline[0] = fetch_stage(instruction_class(),self)
                    self.processor.pipeline[1] = decode_stage(instruction_class(),self)
                    self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                    
                    self.processor.branched = True

            elif self.instr.opcode == "beq":
                if self.instr.opr1Value == self.instr.opr2Value:
                    self.processor.programCounter += int(self.instr.immediate)*4 - 12
                    ## flush pipeline
                    self.processor.pipeline[0] = fetch_stage(instruction_class(),self)
                    self.processor.pipeline[1] = decode_stage(instruction_class(),self)
                    self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                    self.processor.branched = True

            elif self.instr.opcode == "jr":
                if self.instr.opr1Value != self.instr.opr2Value:
                    self.processor.programCounter = int(self.instr.opr1Value)
                    ## flush pipeline  
                    self.processor.pipeline[0] = fetch_stage(instruction_class(),self)
                    self.processor.pipeline[1] = decode_stage(instruction_class(),self)
                    self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                    self.processor.branched = True
            
            elif self.instr.opcode == "slt":
                self.instr.result = 1 if self.instr.opr1Value < self.instr.opr2Value else 0

            elif self.instr.opcode == "nor":
                self.instr.result = ~(int(self.instr.opr1Value) | int(self.instr.opr2Value))
                
            elif self.instr.opcode == "add":
                self.instr.result = int(self.instr.opr1Value) + int(self.instr.opr2Value)

            elif self.instr.opcode == "sub":
                self.instr.result = int(self.instr.opr1Value) - int(self.instr.opr2Value)
                
            elif self.instr.opcode == "or":
                self.instr.result = int(self.instr.opr1Value) | int(self.instr.opr2Value)

            elif self.instr.opcode == "and":
                self.instr.result = int(self.instr.opr1Value) & int(self.instr.opr2Value)
                
            elif self.instr.opcode == "addi":
                self.instr.result = int(self.instr.opr1Value) + int(self.instr.immediate)

            elif self.instr.opcode == "subi":
                self.instr.result = int(self.instr.opr1Value) - int(self.instr.immediate)

            elif self.instr.opcode == "ori":
                self.instr.result = int(self.instr.opr1Value) | int(self.instr.immediate)

            self.instr.result = str(self.instr.result)
