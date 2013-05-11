from control import *
from alu import ALU
from ..components.misc import *
from ..components.registers import *
from ..components.mem import Mem

# It starts with a counter :')
pc = DRegister32()

imem = Mem.with_parameters(width = 32, size = 1024)(addr = pc.d[:], write_en = 0)

control = ControlUnit(opcode = imem[31:26])
alucontrol = ALUControlUnit(aluop = control.aluop[:],
                            funct = imem.read[5:0],
                            opcode = imem.read[31:26])

write_reg_mux = Mux(in0 = imem.read[20:16], in1 = imem.read[15:11], s = control.regdst[:])

regs = RegisterFile.with_parameters(num_regs = 32, width = 32)(
        read_reg1 = imem.read[25:21],
        read_reg2 = imem.read[20:16],
        write_reg = WRITE_REG_MUX.out[:])

inst_sign_ext = SignExt(inp = imem.read[15:0])

alusrc_mux = Mux(in0 = regs.read2[:], in1 = inst_sign_ext.out[:], s = control.alusrc)

alu = ALU(alucontrol = control.alucontrol[:], in0 = regs.read1[:], in1 = alusrc_mux.out[:])

dmem = Mem.with_parameters(width = 32 size = 8192)(
        addr = alu.out[:],
        write = regs.read2[:],
        write_en = control.memwrite[:],
        read_en = control.memread[:])

regs_write_data_mux = Mux(in0 = alu.out[:], in1 = dmem.read[:], s = control.memtoreg)

regs.write = regs_write_data_mux.out[:]

# Now the PC update branch
pc_add4 = Adder32(in0 = pc.d[:], in1 = 4)

address_sll2 = SLL2(inp = inst_sign_ext.out[:])
branch_adder = Adder32(in0 = pc_add4.out[:], in1 = address_sll2.out[:])
branch_and_gate = AndGate(in0 = control.branch[:], in1 = alu.zero[:])
branch_mux = Mux(in0 = pc_add4.out[:], in1 = branch_adder.out[:], s = branch_and_gate.out[:])

jmp_sll2 = SLL2(inp = imem.read[25:0])
pc_update_mux = Mux(in0 = branch_mux.out[:],
                    in1 = Wire(jmp_sll2.out[:], pc_add4.out[31:28]),
                    s   = control.jump[:])

# And it ends with a counter update
pc.q = pc_update_mux.out[:]
