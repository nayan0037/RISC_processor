import re

class instruction_class(object):
    instructionSet = {
        'rtype': ['add', 'sub', 'and', 'or', 'jr', 'nor', 'slt'],
        'itype': ['addi', 'subi', 'ori', 'bne', 'beq', 'lw', 'sw'],
        'jtype': ['j']
    }

    def __init__(self):
        self.instruction = "nop"
        self.opcode = "nop"
        self.operand1 = None
        self.operand2 = None
        self.dest = None
        self.immediate = "0"
        self.aluOp = False
        self.memRead = False
        self.memWrite = False
        self.regRead = False
        self.regWrite = False    
        self.BTA = None
        self.opr1Value = None
        self.opr2Value = None
        self.result = None
        self.is_branch = False
        self.type = None    
        self.forwardEE_opr1 = False
        self.forwardEE_opr2 = False
        self.forwardME_opr1 = False
        self.forwardME_opr2 = False
        self.is_load = False


    def decode(self,instruction):
        # print(instruction)
        # print(type(instruction))
        instruction = instruction.instruction.strip()
        # print(instruction)
        self.instruction = re.sub('\s+',' ',instruction)
        s = self.instruction.split()
        self.opcode = s[0].lower()
        if self.opcode in self.instructionSet['rtype']:
            self.type = "rtype"
            if(self.opcode == "jr"):
                self.operand1 = s[1]
                self.regRead = True
                self.aluOp = True
            else:
                self.dest = s[1]
                self.operand1 = s[2]
                self.operand2 = s[3]
                self.regRead = True
                self.regWrite = True
                self.aluOp = True

        elif self.opcode in self.instructionSet['itype']:
            self.type = "itype"
            if(self.opcode == "lw"):
                self.dest = s[1]
                self.immediate = s[2].split("(")[0]
                self.operand1 = s[2].split("(")[1].split(")")[0]
                self.regRead = True
                self.memRead = True
                self.regWrite = True
                self.aluOp = True
                self.is_load = True

            elif(self.opcode == "sw"):
                self.operand2 = s[1]
                self.immediate = s[2].split("(")[0]
                self.operand1 = s[2].split("(")[1].split(")")[0]
                self.regRead = True
                self.memWrite = True
                self.aluOp = True

            elif(self.opcode == "beq" or self.opcode == "bne"):
                self.operand1 = s[1]
                self.operand2 = s[2]
                self.immediate = s[3]
                self.regRead = True
                self.aluOp = True
                self.is_branch = True

            else:
                self.dest = s[1]
                self.operand1 = s[2]
                self.immediate = s[3]
                self.regRead = True
                self.regWrite = True
                self.aluOp = True

        elif self.opcode in self.instructionSet['jtype']:
            self.type = "jtype"
            if ("0x" in s[1]):
                self.BTA = int(s[1], 16)
            else:
                self.BTA = s[1]

        elif self.opcode == "nop":
            return

        else:
            raise ValueError('Invalid Instruction')

        if ("0x" in self.immediate):
            self.immediate = int(self.immediate, 16)
        else:
            self.immediate = self.immediate
