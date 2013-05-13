__all__ = ['asm', 'control', 'alu', 'MIPSArchitecture', 'layout']

import layout, asm, control, alu
from architecture import new_architecture

MIPSArchitecture = new_architecture('MIPS', 'mips.arch', 'clk')

