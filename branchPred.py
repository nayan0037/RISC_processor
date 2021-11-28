class branchPred(object):
    """docstring for branchPred"""
    def __init__(self,depth):
        self.noPred = False
        self.BTA = [0 for i in range(depth)]
        self.history = ["00" for i in range(depth)]
        self.PC = [0 for i in range(depth)]
        self.BTA_history = ["00" for i in range(depth)]

    def update_pred(self,PC,result,BTA):
        if self.noPred:
            return
        index = self.PC.index(PC)
        if self.history[index] == "00":
            if result == "1":
                self.history[index] = "01"
            else:
                self.history[index] = "00"

        elif self.history[index] == "01":
            if result == "1":
                self.history[index] = "11"
                self.BTA[index] = BTA
            else:
                self.history[index] = "00"

        elif self.history[index] == "10":
            if result == "1":
                self.history[index] = "11"
                self.BTA[index] = BTA
            else:
                self.history[index] = "00"

        elif self.history[index] == "11":
            if result == "1":
                self.history[index] = "11"
            else:
                self.history[index] = "01"

    def predict(self,PC):
        if self.noPred:
            (PC + 4, "0")
        if PC in self.PC:
            index = self.PC.index(PC)
            if (self.history[index][0] == "1"):
                return (self.BTA[index],"1")
            else:
                return (PC+4,"0")
        else:
            self.PC.append(PC)
            self.BTA.append(0)
            self.history.append("00")
            return (0,"0")

    def print_branchPred(self):
        if self.noPred:
            return
        print("PC\tBTA\tHist")
        for i in range(len(self.PC)):
            if(self.PC[i] != 0):
                print("{}\t{}\t{}".format(self.PC[i],self.BTA[i],self.history[i]))







