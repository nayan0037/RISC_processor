class memory_stage():
    """docstring for memory_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        if self.instr.memRead:
            self.result = self.processor.main_memory[self.instr.result]
        elif self.instr.memWrite:
            self.processor.main_memory[self.instr.result] = self.instr.opr2Value
