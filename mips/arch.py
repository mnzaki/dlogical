from mips.control import *
from mips.alu import ALU
from components.misc import *
from components.registers import *
from components.mem import Mem
from components.oscillator import *

clk = Oscillator.with_parameters(freq = 10000)()

# It starts with a counter :')
pc = DRegisterSync32(clk = clk.clk[:])

imem = Mem.with_parameters(width = 32, size = 1024)(
        addr = pc.d[:],
        write_en = 0,
        read_en = 1)

control = ControlUnit(opcode = imem.read[31:26])
alucontrol = ALUControlUnit(aluop = control.aluop[:],
                            funct = imem.read[5:0],
                            opcode = imem.read[31:26])

write_reg_mux = Mux32(in0 = imem.read[20:16], in1 = imem.read[15:11], s = control.regdst[:])
write_reg_ra_mux = Mux32(in0 = write_reg_mux.out[:], in1 = 31, s = control.pctora[:])

regs = RegisterFileSync.with_parameters(num_regs = 32, width = 32)(
        read_reg1 = imem.read[25:21],
        read_reg2 = imem.read[20:16],
        write_reg = write_reg_ra_mux.out[:],
        write_en  = control.regwrite[:],
        clk       = clk.clk[:])

inst_sign_ext = SignExt(inp = imem.read[15:0])

alusrc_mux = Mux32(in0 = regs.read2[:], in1 = inst_sign_ext.out[:], s = control.alusrc[:])

alu = ALU(control = alucontrol.alucontrol[:],
          in0 = regs.read1[:], in1 = alusrc_mux.out[:],
          shamt = imem.read[10:6])

dmem = Mem.with_parameters(width = 32, size = 8192)(
        addr = alu.out[:],
        write = regs.read2[:],
        write_en = control.memwrite[:],
        read_en = control.memread[:])

pc_add4 = Adder32(in0 = pc.d[:], in1 = 4)

regs_write_data_mux = Mux32(in0 = alu.out[:], in1 = dmem.read[:], s = control.memtoreg[:])
regs_write_pc_mux   = Mux32(in0 = regs_write_data_mux.out[:], in1 = pc_add4.out[:], s = control.pctora[:])

regs.write = regs_write_pc_mux.out[:]

# Now the PC update branch

address_sll2 = SLL2(inp = inst_sign_ext.out[:])
branch_adder = Adder32(in0 = pc_add4.out[:], in1 = address_sll2.out[:])
branch_control = BranchControl(branch = control.branch[:], zero = alu.zero[:], eq = control.beq_ne[:])
branch_mux = Mux32(in0 = pc_add4.out[:], in1 = branch_adder.out[:], s = branch_control.out[:])

jmp_sll2 = SLL2(inp = imem.read[25:0])
pc_update_mux = Mux32(in0 = branch_mux.out[:],
                      in1 = Wire(pc_add4.out[31:28], jmp_sll2.out[:]),
                      s   = control.jump[:])

# And it ends with a counter update
pc.q = pc_update_mux.out[:]
