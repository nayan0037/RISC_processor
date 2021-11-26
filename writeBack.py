class writeBack_stage():
    """docstring for writeBack_stage"""
    def __init__(self,instruction,processor):
        self.instr = instruction
        self.processor = processor
        
    def advance(self):
        if self.instr.regWrite:
            if not "$r0" in self.instr.dest:
                self.processor.registers[self.instr.dest] = self.instr.result
