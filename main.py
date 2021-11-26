from memory import memory



R = {i:0 for i in range(8)}
PC = 0
instr = 0

icache = memory(32)

def fetch():
	# iff bubble dont fetch
	return icache.get_value(PC)

def decode():
	opcode = 
	operand1 = 
	operand2 = 
	dest = 
	