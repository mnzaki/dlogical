import unittest
from mips.asm import Assembler
from bitstring import BitArray

class TestMipsAssembler(unittest.TestCase):
  def test_mips_asm1(self):
    assembler = Assembler()
    asm = assembler.assemble('tests/test_mips_asm1.asm')
    expected_asm = [
      '001000' '00000' '01001' '0000' '0000' '0010' '1010',
      '000000' '00000' '01001' '01001' '00010' '000000',
      '100011' '01000' '01010' '0000' '0000' '0000' '0000',
      '000100' '01011' '00000' '1111' '1111' '1111' '1110'
    ]

    asm = list(asm)
    for i, a in enumerate(asm):
      asm[i] = bin(a)[2:].rjust(32, '0')

    self.assertEqual(expected_asm, asm)
