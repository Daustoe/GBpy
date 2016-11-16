import unittest
from cpu import Cpu
from mmu import MMU


class TestArithmeticOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_registers_0_at_init(self):
        self.assertEqual(0, self.cpu.registers.a)
        self.assertEqual(0, self.cpu.registers.b)
        self.assertEqual(0, self.cpu.registers.c)
        self.assertEqual(0, self.cpu.registers.d)
        self.assertEqual(0, self.cpu.registers.e)
        self.assertEqual(0, self.cpu.registers.h)
        self.assertEqual(0, self.cpu.registers.l)

    def test_flags_0_at_init(self):
        self.assertEqual(0, self.cpu.registers.carry_flag)
        self.assertEqual(0, self.cpu.registers.hc_flag)
        self.assertEqual(0, self.cpu.registers.zero_flag)
        self.assertEqual(0, self.cpu.registers.sub_flag)

    def test_direct_add(self):
        self.cpu.registers.b = 0
        self.cpu.registers.c = 15  # should trip sub flag
        self.cpu.registers.d = 255  # should trip carry flag, sub flag reset
        self.cpu.registers.e = 7
        self.cpu.registers.h = 234 # should trip zero flag

        self.cpu._op_80()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertListEqual([1, 0, 0, 0], self.cpu.flags())

        self.cpu.registers.a = 1
        self.cpu._op_81()
        self.assertEqual(self.cpu.registers.a, 16)
        self.assertListEqual([0, 0, 1, 0], self.cpu.flags())

        self.cpu._op_82()
        self.assertEqual(self.cpu.registers.a, 15)
        self.assertListEqual([0, 0, 0, 1], self.cpu.flags())

        self.cpu._op_83()
        self.cpu._op_84()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertListEqual([1, 0, 1, 1], self.cpu.flags())

    def test_direct_adc(self):
        self.cpu.registers.b = 0
        self.cpu.registers.c = 15  # should trip sub flag
        self.cpu.registers.d = 255  # should trip carry flag, sub flag reset
        self.cpu.registers.e = 7
        self.cpu.registers.h = 233  # should trip zero flag

        self.cpu._op_88()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertListEqual([1, 0, 0, 0], self.cpu.flags())

        self.cpu.registers.a = 1
        self.cpu._op_89()
        self.assertEqual(self.cpu.registers.a, 16)
        self.assertListEqual([0, 0, 1, 0], self.cpu.flags())

        self.cpu._op_8a()
        self.assertEqual(self.cpu.registers.a, 15)
        self.assertListEqual([0, 0, 0, 1], self.cpu.flags())

        self.cpu._op_8b()
        self.cpu._op_8c()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertListEqual([1, 0, 1, 1], self.cpu.flags())

    def test_indirect_add(self):
        self.cpu._op_86()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.hc_flag, 0)

        self.cpu._op_c6()
        self.assertEqual(self.cpu.registers.a, 0xfe)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)

    def test_indirect_adc(self):
        self.cpu.registers.a = 1
        self.cpu.registers.sub_flag = 1
        self.cpu._op_8e()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.sub_flag, 0)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)

        self.cpu._op_ce()
        self.assertEqual(self.cpu.registers.a, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 0)
        self.assertEqual(self.cpu.registers.carry_flag, 0)
        self.assertEqual(self.cpu.registers.hc_flag, 0)

    def test_direct_sub(self):
        self.cpu.registers.a = 1
        self.cpu.registers.b = 1
        self.cpu.registers.c = 1
        self.cpu._op_90()
        self.assertEqual(self.cpu.registers.sub_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

        self.cpu._op_91()

    def test_direct_sbc(self):
        self.cpu.registers.b = 1
        self.cpu._op_98()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.sub_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 0)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)

    def test_indirect_sub(self):
        self.cpu.registers.a = 0xff
        self.cpu._op_96()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.sub_flag, 1)

        self.cpu._op_96()
        self.assertEqual(self.cpu.registers.a, 0x01)
        self.assertEqual(self.cpu.registers.zero_flag, 0)
        self.assertEqual(self.cpu.registers.sub_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)
        self.assertEqual(self.cpu.registers.carry_flag, 1)

        self.cpu.registers.a = 0xff
        self.cpu.registers.pc = 0  # Just to be sure
        self.cpu._op_d6()  # subtracts value in memory at location of current PC from A
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.pc, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.sub_flag, 1)
        self.assertEqual(self.cpu.registers.carry_flag, 0)
        self.assertEqual(self.cpu.registers.hc_flag, 0)

    def test_indirect_sbc(self):
        self.cpu._op_9e()
        self.assertEqual(self.cpu.registers.a, 0x01)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 0)
        self.assertEqual(self.cpu.registers.sub_flag, 1)

        self.cpu.registers.pc = 1
        self.cpu._op_de()
        self.assertEqual(self.cpu.registers.a, 0)  # Carry flag is set, so 1-1 = 0
        self.assertEqual(self.cpu.registers.carry_flag, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 0)
        self.assertEqual(self.cpu.registers.sub_flag, 1)


    def test_increment(self):
        self.cpu._op_04()
        self.assertEqual(self.cpu.registers.b, 1)

        self.cpu.registers.c = 0xf
        self.cpu._op_0c()
        self.assertEqual(self.cpu.registers.c, 0x10)
        self.assertEqual(self.cpu.registers.hc_flag, 1)
        self.cpu._op_34()
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)

    def test_decrement(self):
        self.cpu.registers.b = 1
        self.cpu._op_05()
        self.assertEqual(self.cpu.registers.b, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.sub_flag, 1)

        self.assertEqual(self.cpu.mmu.rom[0], 0xff)
        self.cpu._op_35()
        self.assertEqual(self.cpu.mmu.rom[0], 0xfe)


class TestLogicalArithmeticOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_direct_xor(self):
        self.cpu._op_a8()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

        self.cpu.registers.b = 0xf
        self.cpu._op_a8()
        self.assertEqual(self.cpu.registers.a, 0xf)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu.registers.b = 0x5f
        self.cpu._op_a8()
        self.assertEqual(self.cpu.registers.a, 0x50)

    def test_indirect_xor(self):
        self.cpu._op_ae()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu._op_ae()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

    def test_direct_or(self):
        self.cpu.registers.b = 0
        self.cpu._op_b0()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

        self.cpu.registers.b = 0x8
        self.cpu._op_b0()
        self.assertEqual(self.cpu.registers.a, 0x8)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu.registers.b = 0xf7
        self.cpu._op_b0()
        self.assertEqual(self.cpu.registers.a, 0xff)

    def test_indirect_or(self):
        self.cpu._op_b6()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu._op_b6()
        self.assertEqual(self.cpu.registers.a, 0xff)

    def test_and(self):
        self.cpu.registers.b = 0xf
        self.cpu._op_a0()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

        self.cpu.registers.a = 0xff
        self.cpu._op_a6()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu.registers.pc = 1
        self.cpu._op_e6()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.pc, 2)

    def test_compare(self):
        self.cpu._op_b8()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.carry_flag, 0)

        self.cpu._op_be()
        self.assertEqual(self.cpu.registers.zero_flag, 0)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.hc_flag, 1)

        self.cpu.registers.a = 0xff
        self.cpu._op_fe()
        self.assertEqual(self.cpu.registers.zero_flag, 1)
        self.assertEqual(self.cpu.registers.carry_flag, 0)


class TestLoadOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_direct_load(self):
        self.cpu.registers.b = 10

        self.cpu._op_48()
        self.assertEqual(self.cpu.registers.b, self.cpu.registers.c)
        self.assertEqual(self.cpu.registers.c, 10)

    def test_indirect_load_HL(self):
        self.cpu.registers.h = 0x0
        self.cpu.registers.l = 0x0
        self.cpu._op_46()
        self.assertEqual(self.cpu.registers.b, 0xff)  # All GB roms will start with this reset op

    def test_indirect_load_PC(self):
        # Reads from memory at address stored in pc (next byte read)
        self.cpu.registers.pc = 0x0
        self.cpu._op_06()
        self.assertEqual(self.cpu.registers.b, 0xff)  # roms begin with 0xff and that is what we are at.
        self.assertEqual(self.cpu.registers.pc, 0x01)  # pc should increment, as we read next value for load

    def test_indirect_load_inc(self):
        self.cpu._op_22()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.l, 1)
        self.assertEqual(self.cpu.registers.h, 0)

        self.cpu.registers.l = 0xff
        self.cpu._op_22()
        self.assertEqual(self.cpu.registers.l, 0)
        self.assertEqual(self.cpu.registers.h, 1)

    def test_indirect_load_dec(self):
        self.cpu.registers.l = 1
        self.cpu._op_32()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.l, 0)

        self.cpu._op_32()
        self.assertEqual(self.cpu.registers.a, 0xff)
        self.assertEqual(self.cpu.registers.l, 0xff)
        self.assertEqual(self.cpu.registers.h, 0xff)


class TestShiftAndRotateOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_rlca(self):
        self.cpu.registers.a = 0x80  # 1000 0001
        self.cpu._op_07()
        self.assertEqual(self.cpu.registers.a, 1)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

    def test_rla(self):
        self.cpu.registers.a = 0x80
        self.cpu._op_17()
        self.assertEqual(self.cpu.registers.a, 0)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

    def test_rrca(self):
        self.cpu.registers.a = 1
        self.cpu._op_0f()
        self.assertEqual(self.cpu.registers.a, 0x80)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

    def test_rra(self):
        self.cpu.registers.a = 1
        self.cpu._op_1f()
        self.assertEqual(self.cpu.registers.a, 0x0)
        self.assertEqual(self.cpu.registers.carry_flag, 1)
        self.assertEqual(self.cpu.registers.zero_flag, 1)

    def test_rlc(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_rl(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_rrc(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_rr(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_sla(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_sra(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)

    def test_srl(self):
        # TODO: part of extended opcodes
        self.assertTrue(False)


class TestJumpOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_jump_to_addr_nn(self):
        self.cpu._op_c3()
        self.assertEqual(self.cpu.registers.pc, 0xff00)

    def test_jump_to_addr_if(self):
        self.cpu._op_c2()
        self.assertEqual(self.cpu.registers.pc, 0xff00)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu.registers.pc = 0
        self.cpu.registers.zero_flag = 1
        self.cpu._op_ca()
        self.assertEqual(self.cpu.registers.pc, 0xff00)

        self.cpu.registers.pc = 0
        self.cpu._op_d2()
        self.assertEqual(self.cpu.registers.pc, 0xff00)
        self.assertEqual(self.cpu.registers.carry_flag, 0)

        self.cpu.registers.pc = 0
        self.cpu.registers.carry_flag = 1
        self.cpu._op_da()
        self.assertEqual(self.cpu.registers.pc, 0xff00)

    def test_jump_to_address_in_HL(self):
        self.cpu.registers.h = 0
        self.cpu.registers.l = 0x41
        self.cpu._op_e9()
        self.assertEqual(self.cpu.registers.pc, 0x24)

    def test_jump_to_addr_add_n(self):
        self.cpu._op_18()
        self.assertEqual(self.cpu.registers.pc, 0xff)

    def test_jump_to_add_add_n_if(self):
        self.cpu._op_20()
        self.assertEqual(self.cpu.registers.pc, 0xff)
        self.assertEqual(self.cpu.registers.zero_flag, 0)

        self.cpu.registers.pc = 0
        self.cpu.registers.zero_flag = 1
        self.cpu._op_28()
        self.assertEqual(self.cpu.registers.pc, 0xff)

        self.cpu.registers.pc = 0
        self.cpu._op_30()
        self.assertEqual(self.cpu.registers.pc, 0xff)
        self.assertEqual(self.cpu.registers.carry_flag, 0)

        self.cpu.registers.pc = 0
        self.cpu.registers.carry_flag = 1
        self.cpu._op_38()
        self.assertEqual(self.cpu.registers.pc, 0xff)


class TestCallOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')
        self.cpu.mmu.rom[0] = 0x1
        self.cpu.mmu.rom[1] = 0xed
        self.cpu.registers.sp = 0xfffe

    def test_standard_call(self):
        self.cpu._op_cd()
        self.assertEqual(self.cpu.registers.sp, 0xfffc)
        self.assertEqual(self.cpu.registers.pc, 1)
        self.cpu._op_cd()
        self.assertEqual(self.cpu.registers.sp, 0xfffa)
        self.assertEqual(self.cpu.registers.pc, 0xed)

    def test_call_if(self):
        self.cpu._op_c4()
        self.cpu._op_cc()
        self.cpu._op_d4()
        self.cpu._op_dc()
        self.assertTrue(False)


class TestRetOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_standard_return(self):
        self.cpu._op_c9()
        self.assertTrue(False)

    def test_return_if(self):
        self.cpu._op_c0()
        self.cpu._op_c8()
        self.cpu._op_d0()
        self.cpu._op_d8()
        self.assertTrue(False)

    def test_return_enable_interrupts(self):
        self.cpu._op_d9()
        self.assertTrue(False)


class TestStackOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_push(self):
        self.assertTrue(False)

    def test_pop(self):
        self.assertTrue(False)


class TestMiscOpcodes(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu(MMU())
        self.cpu.mmu.rom = [0] * 128
        self.cpu.mmu.load('C:/Users/cjpowell/workspace/Python/gbpy/resources/test_file.gb')

    def test_daa(self):
        self.cpu.registers.a = 0xc9
        self.cpu._op_27()
        self.assertEqual(self.cpu.registers.a, 0x29)
        self.assertEqual(self.cpu.registers.carry_flag, 1)

if __name__ == '__main__':
    unittest.main()