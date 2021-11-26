from instruction import *
from fetch import *
from decode import *
from operandRead import *
from execute import *
from memory import *
from writeBack import *

pipe = ["F","D","O","E","M","W"]


class processor(object):

    def __init__(self,instrSet):
        self.instrCount = 0
        self.cycleCount = 0
        self.hazardList = []
        self.done = False
        self.branched = False
        self.stall = False
        self.nstall = False
        self.hazardType = []
        
        self.pipeline = [None for x in range(6)]
        nop = instruction_class()
        self.pipeline[0] = fetch_stage(nop,self)
        self.pipeline[1] = decode_stage(nop,self)
        self.pipeline[2] = operandRead_stage(nop,self)
        self.pipeline[3] = execute_stage(nop,self)
        self.pipeline[4] = memory_stage(nop,self)
        self.pipeline[5] = writeBack_stage(nop,self)

        self.registers = {"$r"+str(i):"0" for i in range(32)}
        self.prog_memory = {int(i*4):"nop" for i in range(int(0x60/4))}
        self.main_memory = {int(i*4):0 for i in range(int(0x60/4))}
        self.programCounter = 0x0000
        self.instructionSet = instrSet


        #load prog_memory
        for i in range(len(instrSet)):
            self.prog_memory[i*4] = instrSet[i]

    def step(self):
        self.cycleCount += 1
        self.pipeline[5] = writeBack_stage(self.pipeline[4].instr,self)
        self.pipeline[4] = memory_stage(self.pipeline[3].instr,self)
        self.pipeline[3] = execute_stage(self.pipeline[2].instr,self)    
        if self.stall :  
            self.pipeline[3] = execute_stage(instruction_class(),self)    
            self.nstall = False
        else :
            self.pipeline[2] = operandRead_stage(self.pipeline[1].instr,self)
            self.pipeline[1] = decode_stage(self.pipeline[0].instr,self)
            self.pipeline[0] = fetch_stage(instruction_class(), self)

        print("\n")
        print("Clock Count: "+str(self.cycleCount))

        j=0
        for p in self.pipeline:
            p.advance()
            if j == 3:
                forward_text = "\t"
                if p.instr.forwardEE_opr1:
                    forward_text += "forwarded opr 1 EE "
                if p.instr.forwardEE_opr2:
                    forward_text += "forwarded opr 2 EE "
                if p.instr.forwardME_opr1:
                    forward_text += "forwarded opr 1 ME "
                if p.instr.forwardME_opr2:
                    forward_text += "forwarded opr 2 ME "

                print(pipe[j] +": " + p.instr.instruction + forward_text)
            else:
                print(pipe[j] +": " + p.instr.instruction)

            j += 1               
        self.stall = self.nstall

        if (self.pipeline[5].instr.regWrite and self.pipeline[5].instr.dest != "$r0"):
            self.hazardList.pop(0)
            
        if (self.stall or self.branched):
            self.programCounter -= 4
            self.branched = False

        self.check_done()

    def check_done(self):
        self.done = True
        # if(self.cycleCount == 12):
        #     return

        for p in self.pipeline:
            if (p.instr.instruction != "nop"):
                self.done = False
                return

    def run(self):
        while not self.done:
            self.step()
            self.debug()

    def debug(self):
        print("Hazard List : ",self.hazardList)
            
        # if self.stall:
        #     print("current cycle was stalled")
        x= input()

        self.printRegFile()
        self.printMem()
        # print(("<CPI> : " , float(self.cycles) / float(self.instrCount))) 

    def printRegFile(self):
        print ("<Register File>")
        for x in self.registers:
            if self.registers[x] != "0":        
                print (x,':',self.registers[x])

    def printMem(self):
        print ("<Memory>")
        for x in self.main_memory:
            if self.main_memory[x] != 0:        
                print (x,':',self.main_memory[x])
                