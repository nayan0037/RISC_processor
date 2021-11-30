from instruction import *
from fetch import *
from decode import *
from operandRead import *
from execute import *
from memory import *
from writeBack import *
from branchPred import *
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


            if self.instr.is_load or self.instr.is_store:
                self.instr.result = int(self.instr.opr1Value) + int(self.instr.immediate)
            elif self.instr.opcode == "bne":
                self.processor.speculative = False
                if self.instr.opr1Value != self.instr.opr2Value:
                    ## taken
                    PC = self.instr.PC
                    BTA = PC + int(self.instr.immediate)*4 
                    if (self.processor.branch_hist.pop(0) != "1" or self.processor.BTA_hist.pop(0) != BTA):
                        ## flush pipeline
                        self.processor.programCounter = BTA
                        self.processor.pipeline[0] = fetch_stage(instruction_class(),self.processor)
                        self.processor.pipeline[1] = decode_stage(instruction_class(),self.processor)
                        self.processor.pipeline[2] = operandRead_stage(instruction_class(),self.processor)
                        self.processor.instrCount -= 3
                        self.processor.branch_pred.update_pred(self.instr.PC,"1",BTA)
                        
                else:
                    ## not taken
                    PC = self.instr.PC
                    BTA = PC + 4 
                    if (self.processor.branch_hist.pop(0) != "0"):
                    ## flush half pipeline
                        self.processor.programCounter = BTA
                        self.processor.pipeline[2] = operandRead_stage(instruction_class(),self.processor)
                        self.processor.pipeline[1] = decode_stage(instruction_class(),self.processor)
                        self.processor.pipeline[0] = fetch_stage(instruction_class(),self.processor)

                        self.processor.instrCount -= 3
                        self.processor.branch_pred.update_pred(self.instr.PC,"0",BTA)
                    # else do nothing

            elif self.instr.opcode == "beq":
                self.processor.speculative = False
                if self.instr.opr1Value == self.instr.opr2Value:
                    ## taken
                    PC = self.instr.PC
                    BTA = PC + int(self.instr.immediate)*4 
                    if (self.processor.branch_hist.pop(0) != "1" or self.processor.BTA_hist.pop(0) != BTA):
                        ## flush pipeline
                        self.processor.programCounter = BTA
                        self.processor.pipeline[0] = fetch_stage(instruction_class(),self)
                        self.processor.pipeline[1] = decode_stage(instruction_class(),self)
                        self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                        self.processor.instrCount -= 3
                        self.processor.branch_pred.update_pred(self.instr.PC,"1",BTA)
                    else:
                        self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                        self.processor.instrCount -= 1

                else:
                    ## not taken
                    PC = self.instr.PC
                    BTA = PC + 4 
                    if (self.processor.branch_hist.pop(0) != "0"):
                    ## flush half pipeline
                        self.processor.programCounter = BTA
                        self.processor.pipeline[2] = operandRead_stage(instruction_class(),self)
                        self.processor.pipeline[1] = decode_stage(instruction_class(),self)
                        self.processor.pipeline[0] = fetch_stage(instruction_class(),self)

                        self.processor.instrCount -= 3
                        self.processor.branch_pred.update_pred(self.instr.PC,"0",BTA)
                    # else do nothing

            
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
