import sys

from processor import *
from pprint import pprint

def parseFile(filename):
    with open(filename) as f:
        data = list(filter((lambda x: x != '\n'), f.readlines()))
        instructions = [(a.replace(',',' ').strip().split("#")[0]) for a in data]
        return instructions

def main():
    instructions = parseFile(sys.argv[1])
    MIPS = processor(instructions)
    print("Press <ENTER> to step")
    x= input()
    MIPS.run()

if __name__ == "__main__":
    main()
