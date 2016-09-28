__author__ = 'Clayton Powell'
import os


class Cpu(object):
    """
    Cpu class that emulates the GameBoy cpu for the emulator.
    """

    def __init__(self, mmu):
        self.pc = 0x100  # Program Counter
        self.previous_pc = 0
        self.sp = 0xfffe  # Stack Pointer
        self.mmu = mmu  # Memory Management Unit
        self.opcode = 0
        self.interrupts = False

        # Registers
        self.a = 0x01
        self.b = 0
        self.c = 0x13
        self.d = 0
        self.e = 0xd8
        self.h = 0x01
        self.l = 0x4d

        # clock values
        self.m = 0
        self.t = 0
        self.clock = {'m': self.m, 't': self.t}

        # we keep the flags separate instead of in the f register. No need to complicate this process.
        self.zero_flag = 1     # 0x80
        self.sub_flag = 0      # 0x40
        self.hc_flag = 1       # 0x20
        self.carry_flag = 1    # 0x10

        # Opcode map, some opcodes not supported in GB architecture
        self.opcodes = {
            0x00: self._op_00,
            0x01: self._op_01,
            0x02: self._op_02,
            0x03: self._op_03,
            0x04: self._op_04,
            0x05: self._op_05,
            0x06: self._op_06,
            0x07: self._op_07,
            0x08: self._op_08,
            0x09: self._op_09,
            0x0a: self._op_0a,
            0x0b: self._op_0b,
            0x0c: self._op_0c,
            0x0d: self._op_0d,
            0x0e: self._op_0e,
            0x0f: self._op_0f,
            0x10: self._op_10,
            0x11: self._op_11,
            0x12: self._op_12,
            0x13: self._op_13,
            0x14: self._op_14,
            0x15: self._op_15,
            0x16: self._op_16,
            0x17: self._op_17,
            0x18: self._op_18,
            0x19: self._op_19,
            0x1a: self._op_1a,
            0x1b: self._op_1b,
            0x1c: self._op_1c,
            0x1d: self._op_1d,
            0x1e: self._op_1e,
            0x1f: self._op_1f,
            0x20: self._op_20,
            0x21: self._op_21,
            0x22: self._op_22,
            0x23: self._op_23,
            0x24: self._op_24,
            0x25: self._op_25,
            0x26: self._op_26,
            0x27: self._op_27,
            0x28: self._op_28,
            0x29: self._op_29,
            0x2a: self._op_2a,
            0x2b: self._op_2b,
            0x2c: self._op_2c,
            0x2d: self._op_2d,
            0x2e: self._op_2e,
            0x2f: self._op_2f,
            0x30: self._op_30,
            0x31: self._op_31,
            0x32: self._op_32,
            0x33: self._op_33,
            0x34: self._op_34,
            0x35: self._op_35,
            0x36: self._op_36,
            0x37: self._op_37,
            0x38: self._op_38,
            0x39: self._op_39,
            0x3a: self._op_3a,
            0x3b: self._op_3b,
            0x3c: self._op_3c,
            0x3d: self._op_3d,
            0x3e: self._op_3e,
            0x3f: self._op_3f,
            0x40: self._op_40,
            0x41: self._op_41,
            0x42: self._op_42,
            0x43: self._op_43,
            0x44: self._op_44,
            0x45: self._op_45,
            0x46: self._op_46,
            0x47: self._op_47,
            0x48: self._op_48,
            0x49: self._op_49,
            0x4a: self._op_4a,
            0x4b: self._op_4b,
            0x4c: self._op_4c,
            0x4d: self._op_4d,
            0x4e: self._op_4e,
            0x4f: self._op_4f,
            0x50: self._op_50,
            0x51: self._op_51,
            0x52: self._op_52,
            0x53: self._op_53,
            0x54: self._op_54,
            0x55: self._op_55,
            0x56: self._op_56,
            0x57: self._op_57,
            0x58: self._op_58,
            0x59: self._op_59,
            0x5a: self._op_5a,
            0x5b: self._op_5b,
            0x5c: self._op_5c,
            0x5d: self._op_5d,
            0x5e: self._op_5e,
            0x5f: self._op_5f,
            0x60: self._op_60,
            0x61: self._op_61,
            0x62: self._op_62,
            0x63: self._op_63,
            0x64: self._op_64,
            0x65: self._op_65,
            0x66: self._op_66,
            0x67: self._op_67,
            0x68: self._op_68,
            0x69: self._op_69,
            0x6a: self._op_6a,
            0x6b: self._op_6b,
            0x6c: self._op_6c,
            0x6d: self._op_6d,
            0x6e: self._op_6e,
            0x6f: self._op_6f,
            0x70: self._op_70,
            0x71: self._op_71,
            0x72: self._op_72,
            0x73: self._op_73,
            0x74: self._op_74,
            0x75: self._op_75,
            0x76: self._op_76,
            0x77: self._op_77,
            0x78: self._op_78,
            0x79: self._op_79,
            0x7a: self._op_7a,
            0x7b: self._op_7b,
            0x7c: self._op_7c,
            0x7d: self._op_7d,
            0x7e: self._op_7e,
            0x7f: self._op_7f,
            0x80: self._op_80,
            0x81: self._op_81,
            0x82: self._op_82,
            0x83: self._op_83,
            0x84: self._op_84,
            0x85: self._op_85,
            0x86: self._op_86,
            0x87: self._op_87,
            0x88: self._op_88,
            0x89: self._op_89,
            0x8a: self._op_8a,
            0x8b: self._op_8b,
            0x8c: self._op_8c,
            0x8d: self._op_8d,
            0x8e: self._op_8e,
            0x8f: self._op_8f,
            0x90: self._op_90,
            0x91: self._op_91,
            0x92: self._op_92,
            0x93: self._op_93,
            0x94: self._op_94,
            0x95: self._op_95,
            0x96: self._op_96,
            0x97: self._op_97,
            0x98: self._op_98,
            0x99: self._op_99,
            0x9a: self._op_9a,
            0x9b: self._op_9b,
            0x9c: self._op_9c,
            0x9d: self._op_9d,
            0x9e: self._op_9e,
            0x9f: self._op_9f,
            0xa0: self._op_a0,
            0xa1: self._op_a1,
            0xa2: self._op_a2,
            0xa3: self._op_a3,
            0xa4: self._op_a4,
            0xa5: self._op_a5,
            0xa6: self._op_a6,
            0xa7: self._op_a7,
            0xa8: self._op_a8,
            0xa9: self._op_a9,
            0xaa: self._op_aa,
            0xab: self._op_ab,
            0xac: self._op_ac,
            0xad: self._op_ad,
            0xae: self._op_ae,
            0xaf: self._op_af,
            0xb0: self._op_b0,
            0xb1: self._op_b1,
            0xb2: self._op_b2,
            0xb3: self._op_b3,
            0xb4: self._op_b4,
            0xb5: self._op_b5,
            0xb6: self._op_b6,
            0xb7: self._op_b7,
            0xb8: self._op_b8,
            0xb9: self._op_b9,
            0xba: self._op_ba,
            0xbb: self._op_bb,
            0xbc: self._op_bc,
            0xbd: self._op_bd,
            0xbe: self._op_be,
            0xbf: self._op_bf,
            0xc0: self._op_c0,
            0xc1: self._op_c1,
            0xc2: self._op_c2,
            0xc3: self._op_c3,
            0xc4: self._op_c4,
            0xc5: self._op_c5,
            0xc6: self._op_c6,
            0xc7: self._op_c7,
            0xc8: self._op_c8,
            0xc9: self._op_c9,
            0xca: self._op_ca,
            0xcb: self._op_cb,
            0xcc: self._op_cc,
            0xcd: self._op_cd,
            0xce: self._op_ce,
            0xcf: self._op_cf,
            0xd0: self._op_d0,
            0xd1: self._op_d1,
            0xd2: self._op_d2,
            0xd3: self._op_d3,
            0xd4: self._op_d4,
            0xd5: self._op_d5,
            0xd6: self._op_d6,
            0xd7: self._op_d7,
            0xd8: self._op_d8,
            0xd9: self._op_d9,
            0xda: self._op_da,
            0xdb: self._op_db,
            0xdc: self._op_dc,
            0xdd: self._op_dd,
            0xde: self._op_de,
            0xdf: self._op_df,
            0xe0: self._op_e0,
            0xe1: self._op_e1,
            0xe2: self._op_e2,
            0xe3: self._op_e3,
            0xe4: self._op_e4,
            0xe5: self._op_e5,
            0xe6: self._op_e6,
            0xe7: self._op_e7,
            0xe8: self._op_e8,
            0xe9: self._op_e9,
            0xea: self._op_ea,
            0xeb: self._op_eb,
            0xec: self._op_ec,
            0xed: self._op_ed,
            0xee: self._op_ee,
            0xef: self._op_ef,
            0xf0: self._op_f0,
            0xf1: self._op_f1,
            0xf2: self._op_f2,
            0xf3: self._op_f3,
            0xf4: self._op_f4,
            0xf5: self._op_f5,
            0xf6: self._op_f6,
            0xf7: self._op_f7,
            0xf8: self._op_f8,
            0xf9: self._op_f9,
            0xfa: self._op_fa,
            0xfb: self._op_fb,
            0xfc: self._op_fc,
            0xfd: self._op_fd,
            0xfe: self._op_fe,
            0xff: self._op_ff,
        }
        self.ext_opcodes = {
            0x00: self._op_cb_00,
            0x01: self._op_cb_01,
            0x02: self._op_cb_02,
            0x03: self._op_cb_03,
            0x04: self._op_cb_04,
            0x05: self._op_cb_05,
            0x06: self._op_cb_06,
            0x07: self._op_cb_07,
            0x08: self._op_cb_08,
            0x09: self._op_cb_09,
            0x0a: self._op_cb_0a,
            0x0b: self._op_cb_0b,
            0x0c: self._op_cb_0c,
            0x0d: self._op_cb_0d,
            0x0e: self._op_cb_0e,
            0x0f: self._op_cb_0f,
            0x10: self._op_cb_10,
            0x11: self._op_cb_11,
            0x12: self._op_cb_12,
            0x13: self._op_cb_13,
            0x14: self._op_cb_14,
            0x15: self._op_cb_15,
            0x16: self._op_cb_16,
            0x17: self._op_cb_17,
            0x18: self._op_cb_18,
            0x19: self._op_cb_19,
            0x1a: self._op_cb_1a,
            0x1b: self._op_cb_1b,
            0x1c: self._op_cb_1c,
            0x1d: self._op_cb_1d,
            0x1e: self._op_cb_1e,
            0x1f: self._op_cb_1f,
            0x20: self._op_cb_20,
            0x21: self._op_cb_21,
            0x22: self._op_cb_22,
            0x23: self._op_cb_23,
            0x24: self._op_cb_24,
            0x25: self._op_cb_25,
            0x26: self._op_cb_26,
            0x27: self._op_cb_27,
            0x28: self._op_cb_28,
            0x29: self._op_cb_29,
            0x2a: self._op_cb_2a,
            0x2b: self._op_cb_2b,
            0x2c: self._op_cb_2c,
            0x2d: self._op_cb_2d,
            0x2e: self._op_cb_2e,
            0x2f: self._op_cb_2f,
            0x30: self._op_cb_30,
            0x31: self._op_cb_31,
            0x32: self._op_cb_32,
            0x33: self._op_cb_33,
            0x34: self._op_cb_34,
            0x35: self._op_cb_35,
            0x36: self._op_cb_36,
            0x37: self._op_cb_37,
            0x38: self._op_cb_38,
            0x39: self._op_cb_39,
            0x3a: self._op_cb_3a,
            0x3b: self._op_cb_3b,
            0x3c: self._op_cb_3c,
            0x3d: self._op_cb_3d,
            0x3e: self._op_cb_3e,
            0x3f: self._op_cb_3f,
            0x40: self._op_cb_40,
            0x41: self._op_cb_41,
            0x42: self._op_cb_42,
            0x43: self._op_cb_43,
            0x44: self._op_cb_44,
            0x45: self._op_cb_45,
            0x46: self._op_cb_46,
            0x47: self._op_cb_47,
            0x48: self._op_cb_48,
            0x49: self._op_cb_49,
            0x4a: self._op_cb_4a,
            0x4b: self._op_cb_4b,
            0x4c: self._op_cb_4c,
            0x4d: self._op_cb_4d,
            0x4e: self._op_cb_4e,
            0x4f: self._op_cb_4f,
            0x50: self._op_cb_50,
            0x51: self._op_cb_51,
            0x52: self._op_cb_52,
            0x53: self._op_cb_53,
            0x54: self._op_cb_54,
            0x55: self._op_cb_55,
            0x56: self._op_cb_56,
            0x57: self._op_cb_57,
            0x58: self._op_cb_58,
            0x59: self._op_cb_59,
            0x5a: self._op_cb_5a,
            0x5b: self._op_cb_5b,
            0x5c: self._op_cb_5c,
            0x5d: self._op_cb_5d,
            0x5e: self._op_cb_5e,
            0x5f: self._op_cb_5f,
            0x60: self._op_cb_60,
            0x61: self._op_cb_61,
            0x62: self._op_cb_62,
            0x63: self._op_cb_63,
            0x64: self._op_cb_64,
            0x65: self._op_cb_65,
            0x66: self._op_cb_66,
            0x67: self._op_cb_67,
            0x68: self._op_cb_68,
            0x69: self._op_cb_69,
            0x6a: self._op_cb_6a,
            0x6b: self._op_cb_6b,
            0x6c: self._op_cb_6c,
            0x6d: self._op_cb_6d,
            0x6e: self._op_cb_6e,
            0x6f: self._op_cb_6f,
            0x70: self._op_cb_70,
            0x71: self._op_cb_71,
            0x72: self._op_cb_72,
            0x73: self._op_cb_73,
            0x74: self._op_cb_74,
            0x75: self._op_cb_75,
            0x76: self._op_cb_76,
            0x77: self._op_cb_77,
            0x78: self._op_cb_78,
            0x79: self._op_cb_79,
            0x7a: self._op_cb_7a,
            0x7b: self._op_cb_7b,
            0x7c: self._op_cb_7c,
            0x7d: self._op_cb_7d,
            0x7e: self._op_cb_7e,
            0x7f: self._op_cb_7f,
            0x80: self._op_cb_80,
            0x81: self._op_cb_81,
            0x82: self._op_cb_82,
            0x83: self._op_cb_83,
            0x84: self._op_cb_84,
            0x85: self._op_cb_85,
            0x86: self._op_cb_86,
            0x87: self._op_cb_87,
            0x88: self._op_cb_88,
            0x89: self._op_cb_89,
            0x8a: self._op_cb_8a,
            0x8b: self._op_cb_8b,
            0x8c: self._op_cb_8c,
            0x8d: self._op_cb_8d,
            0x8e: self._op_cb_8e,
            0x8f: self._op_cb_8f,
            0x90: self._op_cb_90,
            0x91: self._op_cb_91,
            0x92: self._op_cb_92,
            0x93: self._op_cb_93,
            0x94: self._op_cb_94,
            0x95: self._op_cb_95,
            0x96: self._op_cb_96,
            0x97: self._op_cb_97,
            0x98: self._op_cb_98,
            0x99: self._op_cb_99,
            0x9a: self._op_cb_9a,
            0x9b: self._op_cb_9b,
            0x9c: self._op_cb_9c,
            0x9d: self._op_cb_9d,
            0x9e: self._op_cb_9e,
            0x9f: self._op_cb_9f,
            0xa0: self._op_cb_a0,
            0xa1: self._op_cb_a1,
            0xa2: self._op_cb_a2,
            0xa3: self._op_cb_a3,
            0xa4: self._op_cb_a4,
            0xa5: self._op_cb_a5,
            0xa6: self._op_cb_a6,
            0xa7: self._op_cb_a7,
            0xa8: self._op_cb_a8,
            0xa9: self._op_cb_a9,
            0xaa: self._op_cb_aa,
            0xab: self._op_cb_ab,
            0xac: self._op_cb_ac,
            0xad: self._op_cb_ad,
            0xae: self._op_cb_ae,
            0xaf: self._op_cb_af,
            0xb0: self._op_cb_b0,
            0xb1: self._op_cb_b1,
            0xb2: self._op_cb_b2,
            0xb3: self._op_cb_b3,
            0xb4: self._op_cb_b4,
            0xb5: self._op_cb_b5,
            0xb6: self._op_cb_b6,
            0xb7: self._op_cb_b7,
            0xb8: self._op_cb_b8,
            0xb9: self._op_cb_b9,
            0xba: self._op_cb_ba,
            0xbb: self._op_cb_bb,
            0xbc: self._op_cb_bc,
            0xbd: self._op_cb_bd,
            0xbe: self._op_cb_be,
            0xbf: self._op_cb_bf,
            0xc0: self._op_cb_c0,
            0xc1: self._op_cb_c1,
            0xc2: self._op_cb_c2,
            0xc3: self._op_cb_c3,
            0xc4: self._op_cb_c4,
            0xc5: self._op_cb_c5,
            0xc6: self._op_cb_c6,
            0xc7: self._op_cb_c7,
            0xc8: self._op_cb_c8,
            0xc9: self._op_cb_c9,
            0xca: self._op_cb_ca,
            0xcb: self._op_cb_cb,
            0xcc: self._op_cb_cc,
            0xcd: self._op_cb_cd,
            0xce: self._op_cb_ce,
            0xcf: self._op_cb_cf,
            0xd0: self._op_cb_d0,
            0xd1: self._op_cb_d1,
            0xd2: self._op_cb_d2,
            0xd3: self._op_cb_d3,
            0xd4: self._op_cb_d4,
            0xd5: self._op_cb_d5,
            0xd6: self._op_cb_d6,
            0xd7: self._op_cb_d7,
            0xd8: self._op_cb_d8,
            0xd9: self._op_cb_d9,
            0xda: self._op_cb_da,
            0xdb: self._op_cb_db,
            0xdc: self._op_cb_dc,
            0xdd: self._op_cb_dd,
            0xde: self._op_cb_de,
            0xdf: self._op_cb_df,
            0xe0: self._op_cb_e0,
            0xe1: self._op_cb_e1,
            0xe2: self._op_cb_e2,
            0xe3: self._op_cb_e3,
            0xe4: self._op_cb_e4,
            0xe5: self._op_cb_e5,
            0xe6: self._op_cb_e6,
            0xe7: self._op_cb_e7,
            0xe8: self._op_cb_e8,
            0xe9: self._op_cb_e9,
            0xea: self._op_cb_ea,
            0xeb: self._op_cb_eb,
            0xec: self._op_cb_ec,
            0xed: self._op_cb_ed,
            0xee: self._op_cb_ee,
            0xf0: self._op_cb_f0,
            0xf1: self._op_cb_f1,
            0xf2: self._op_cb_f2,
            0xf3: self._op_cb_f3,
            0xf4: self._op_cb_f4,
            0xf5: self._op_cb_f5,
            0xf6: self._op_cb_f6,
            0xf7: self._op_cb_f7,
            0xf8: self._op_cb_f8,
            0xf9: self._op_cb_f9,
            0xfa: self._op_cb_fa,
            0xfb: self._op_cb_fb,
            0xfc: self._op_cb_fc,
            0xfd: self._op_cb_fd,
            0xfe: self._op_cb_fe,
            0xff: self._op_cb_ff,
        }

    def cycle(self):
        """
        Single cpu cycle. Reads opcode at program counter in memory. Executes that opcode.
        """
        self.previous_pc = self.pc
        self.opcode = self.mmu.read_byte(self.pc)

        print('PC:\t' + hex(self.pc))
        print('SP:\t' + hex(self.sp) + '\n')
        print('A: \t' + hex(self.a))
        print('B: \t' + hex(self.b))
        print('C: \t' + hex(self.c))
        print('D: \t' + hex(self.d))
        print('E: \t' + hex(self.e))
        print('H: \t' + hex(self.h))
        print('L: \t' + hex(self.l) + '\n')
        print('Flags:')
        print('\tZ: ' + str(self.zero_flag) + '\tN: ' + str(self.sub_flag) + '\tH: ' + str(self.hc_flag) + '\tC: ' + str(self.carry_flag))
        print('\n')

        self.pc += 1
        self.opcodes[self.opcode]()
        self.pc &= 0xffff
        self.clock['m'] = self.m

    def registers(self):
        return [self.a, self.b, self.c, self.d, self.e, self.h, self.l]

    def flags(self):
        return [self.zero_flag, self.sub_flag, self.hc_flag, self.carry_flag]

    def _rst(self, pc):
        """
        Push present program counter (pc) onto stack. Jump to new pc given.
        :param pc:
        :return:
        """
        self.sp = (self.sp - 2) & 0xffff
        call_addr = self.mmu.read_byte(self.pc)
        call_addr += self.mmu.read_byte(self.pc + 1) << 8
        self.pc = pc

    def _cp(self, value):
        """
        Compare A with value. Results are not kept in A. This op does not affect registers in any way.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if A < n

        :param value:
        :return:
        """
        self.sub_flag = 1
        if self.a == value:
            self.zero_flag = 1
        else:
            self.zero_flag = 0
        if self.a < value:
            self.carry_flag = 1
        else:
            self.carry_flag = 0
        if (self.a & 0xf) < (value & 0xf):
            self.hc_flag = 1
        else:
            self.hc_flag = 0

    def _inc(self, register):
        """
        Increment register.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected

        :param register:
        :return:
        """
        temp = getattr(self, register) + 1
        setattr(self, register, temp)
        self.zero_flag = 1 if temp == 0 else 0
        self.sub_flag = 0
        self.hc_flag = 1 if (temp & 0xf) == 0 else 0

    def _dec(self, register):
        """
        Decrement register.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if no borrow from bit 3.
        C - Not affected

        :param register:
        :return:
        """
        temp = getattr(self, register) - 1
        setattr(self, register, temp)
        self.zero_flag = 1 if temp == 0 else 0
        self.sub_flag = 1
        self.hc_flag = 1 if (temp & 0xf) > 0xf else 0  # TODO: May have to modify, should be now borrow but is carry

    def _add(self, value):
        """
        Add value to register A.

        Flags affected:
        Z - Set if result is zero.
        N - Reset to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7

        :param value:
        :return:
        """
        self.hc_flag = 1 if ((self.a & 0xf) + (value & 0xf)) > 0xf else 0
        self.a += value
        self.carry_flag = 1 if self.a > 0xff else 0
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 0

    def _sub(self, value):
        """
        Subtract value from register A.

        Flags affected:
        z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow

        :param value:
        :return:
        """
        self.hc_flag = 1 if (self.a & 0xf) < (value & 0xf) else 0
        self.carry_flag = 1 if self.a < value else 0
        self.a -= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 1

    def _and(self, value):
        """
        Logically AND value with register A. Store result in register A.

        Flags affected:
        Z - Set if result is zero
        N - Reset to 0
        H - Set to 1
        C - Reset to 0

        :param value:
        :return:
        """
        self.a &= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.hc_flag = 1
        self.sub_flag = 0
        self.carry_flag = 0

    def _or(self, value):
        """
        Logical OR abstracted method used by OR opcodes. All OR operations compare the given value with the
        Accumulator register (register A) whether that value be from memory or from another register.
        :param value:
        :return:
        """
        self.a |= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.carry_flag = 0
        self.hc_flag = 0
        self.sub_flag = 0

    def _xor(self, value):
        """
        Logical XOR abstracted method used for XOR opcodes. All XOR operations compare a value to the
        Accumulator register (register A) whether that value be from memory or from another register.
        :param value:
        :return:
        """
        self.a ^= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.carry_flag = 0
        self.hc_flag = 0
        self.sub_flag = 0

    def _op_00(self):
        """
        NOP
        0x00
        :return:
        4
        """
        return 4

    def _op_01(self):
        """
        LD BC, d16
        0x01
        :return:
        """
        self.c = self.mmu.read_byte(self.pc)
        self.b = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        return 12

    def _op_02(self):
        """
        LD (BC), A
        0x02
        :return:
        """
        self.mmu.write_byte((self.b << 8) + self.c, self.a)
        return 8

    def _op_03(self):
        """
        INC BC
        Increment register pair BC.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self.c = (self.c + 1) & 0xff
        if self.c == 0:
            self.b = (self.b + 1) & 0xff
        return 8

    def _op_04(self):
        """
        INC B
        Increment register B.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('b')
        return 4

    def _op_05(self):
        """
        DEC B
        0x05
        :return:
        """
        self._dec('b')
        return 4

    def _op_06(self):
        """
        LD B, d8
        0x06
        :return:
        """
        self.b = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_07(self):
        """
        RLCA
        Rotate A left. Old bit 7 to Carry flag.

        Flags affected:
        Z - set if result is zero
        N - set to 0
        H - set to 0
        C - Contains old bit 7 data

        0x07
        :return:
        """
        self.carry_flag = (self.a & 0x80) // 0x80
        self.a = ((self.a << 1) & 0xff) | self.carry_flag
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 0
        self.hc_flag = 0
        return 4

    def _op_08(self):
        """
        LD (a16), SP
        0x08
        :return:
        """
        self.mmu.write_word(self.pc, self.sp)
        return 20

    def _op_09(self):
        """
        ADD HL, BC
        Add register pair BC to HL.

        Flags affected:
        Z - Not affected
        N - Reset to 0
        H - Set if carry from bit 11
        C - Set if carry from bit 15
        :return:
        """
        hl = (self.h << 8) + self.l
        bc = (self.b << 8) + self.c
        if hl + bc > 0xffff:
            self.carry_flag |= 1
        if (hl & 0x0fff) + (bc & 0x0fff) > 0x0fff:
            self.hc_flag |= 1
        hl = (hl + bc) & 0xffff
        self.h = hl >> 8
        self.l = hl & 0xff
        return 8

    def _op_0a(self):
        """
        LD A, (BC)
        0x0a
        :return:
        """
        self.a = self.mmu.read_byte((self.b << 8) | self.c)
        return 8

    def _op_0b(self):
        """
        DEC BC
        0x0b
        :return:
        """
        self.c = (self.c - 1) & 0xff
        if self.c == 0xff:
            self.b = (self.b - 1) & 0xff
        return 8

    def _op_0c(self):
        """
        INC C
        Increment register C.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected

        :return:
        """
        self._inc('c')
        return 4

    def _op_0d(self):
        """
        DEC C
        0x0d
        :return:
        """
        self._dec('c')
        return 4

    def _op_0e(self):
        """
        LD C, d8
        0x0e
        :return:
        """
        self.c = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_0f(self):
        """
        RRCA
        Rotate A right. Old bit 0 to Carry flag.

        Flags affected:
        Z - set if result is zero
        N - set to 0
        H - set to 0
        C - contains old bit 0 data
        0x0f
        :return:
        """
        self.carry_flag = self.a & 0x1
        self.a = ((self.a >> 1) & 0xff) | (self.carry_flag * 0x80)
        self.sub_flag = 0
        self.hc_flag = 0
        self.zero_flag = 1 if self.a == 0 else 0
        return 4

    def _op_10(self):
        """
        STOP 0
        0x10
        :return:
        """
        # TODO: Once cycles implemented, add functionality to stop cycles here.
        return 4

    def _op_11(self):
        """
        LD DE, d16
        0x11
        :return:
        """
        self.e = self.mmu.read_byte(self.pc)
        self.d = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        return 12

    def _op_12(self):
        """
        LD (DE), A
        Load value in memory at address in register pair DE into register A.
        :return:
        """
        self.mmu.write_byte((self.d << 8) + self.e, self.a)
        return 8

    def _op_13(self):
        """
        INC DE
        Increment register pair DE.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self.e = (self.e + 1) & 0xff
        if self.e == 0:
            self.d = (self.d + 1) & 0xff
        return 8

    def _op_14(self):
        """
        INC D
        Increment register D.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('d')
        return 4

    def _op_15(self):
        """
        DEC D
        Decrement register D.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        # DEC D
        self._dec('d')
        return 4

    def _op_16(self):
        # LD D, d8
        self.d = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_17(self):
        """
        RLA
        Rotate A left through Carry flag.
        :return:
        """
        high_bit = (self.a & 0x80) << 7
        self.a = ((self.a << 1) & 0xff) | self.carry_flag
        self.carry_flag = high_bit
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 0
        self.hc_flag = 0
        return 4

    def _op_18(self):
        """
        JR n
        Add n to current address (pc) and jump to it.
        :return:
        """
        delta = self.mmu.read_byte(self.pc)
        self.pc += 1
        if delta > 0x7f:
            delta -= 0x100
        self.pc += delta
        return 12

    def _op_19(self):
        """
        Add HL, DE
        Add DE register pair to HL.

        Flags affected:
        Z - Not affected
        N - Reset to 0
        H - Set if carry from bit 11
        C - Set if carry from bit 15
        :return:
        """
        hl = (self.h << 8) + self.l
        de = (self.d << 8) + self.e
        if hl + de > 0xffff:
            self.carry_flag |= 1
        if (hl & 0x0fff) + (de & 0x0fff) > 0x0fff:
            self.hc_flag |= 1
        hl = (hl + de) & 0xffff
        self.h = hl >> 8
        self.l = hl & 0xff
        return 8

    def _op_1a(self):
        # LD A, (DE)
        self.a = self.mmu.read_byte((self.d << 8) | self.e)
        return 8

    def _op_1b(self):
        """
        DEC DE
        Decrement register DE
        :return:
        """
        self.e = (self.e - 1) & 0xff
        if self.e == 0xff:
            self.d = (self.d - 1) & 0xff
        return 8

    def _op_1c(self):
        """
        INC E
        Increment register.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('e')
        return 4

    def _op_1d(self):
        # DEC E
        self._dec('e')
        return 4

    def _op_1e(self):
        # LD E, d8
        self.e = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_1f(self):
        """
        RRA
        Rotate A right through Carry Flag.

        Flags affected:
        Z - set if result is zero
        N - set to 0
        H - set to 0
        C - contains old bit 0 data
        :return:
        """
        low_bit = self.a & 0x1
        self.a = ((self.a >> 1) & 0xff) | (self.carry_flag * 0x80)
        self.carry_flag = low_bit
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 0
        self.hc_flag = 0
        return 4

    def _op_20(self):
        """
        JR NZ, nn
        If zero flag == 0 then add n to current address and jump to it.
        :return:
        """
        if self.zero_flag == 0:
            return self._op_18()
        else:
            self.pc += 1
            return 8

    def _op_21(self):
        # LD HL, d16
        self.l = self.mmu.read_byte(self.pc)
        self.h = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        return 12

    def _op_22(self):
        # LD (HL+), A
        # TODO: is this increment HL or increment memory at addr HL?
        self.mmu.write_byte((self.h << 8) + self.l, self.a)
        self.l = (self.l + 1) & 0xff
        if self.l == 0:
            self.h = (self.h + 1) & 0xff
        return 8

    def _op_23(self):
        """
        INC HL
        Increment register pair HL.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self.l = (self.l + 1) & 0xff
        if self.l == 0:
            self.h = (self.h + 1) & 0xff
        return 4
        return 8

    def _op_24(self):
        """
        INC H
        Increment register H.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('h')
        return 4

    def _op_25(self):
        """
        DEC H
        Decrement register H.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if carry from bit 3
        C - Not affected
        :return:
        """
        self._dec('h')
        return 4

    def _op_26(self):
        """
        LD H, d8
        Load immediate byte value into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_27(self):
        """
        DAA
        Decimal adjust register A.
        This instruction adjusts register A so that the correct representation of Binary Coded Decimal (BCD)
        is obtained.

        Flags affected:
        Z - Set if register A is zero
        N - no affected
        H - set to 0
        C - set if register carries over 0xff
        :return:
        """
        if not self.sub_flag:
            if self.hc_flag or (self.a & 0xf) > 0x9:
                self.a += 0x06
            if self.carry_flag or self.a > 0x9f:
                self.a += 0x60
        else:
            if self.hc_flag:
                self.a = (self.a - 0x06) & 0xff
            if self.carry_flag:
                self.a -= 0x60
        if self.a == 0:
            self.zero_flag = 1
        self.hc_flag = 0
        if (self.a & 0x100) == 0x100:
            self.carry_flag = 1
        self.a &= 0xff
        return 4

    def _op_28(self):
        """
        JR NZ, nn
        If zero flag == 1 then add n to current address and jump to it.
        :return:
        """
        if self.zero_flag:
            return self._op_18()
        else:
            self.pc += 1
            return 8

    def _op_29(self):
        """
        ADD HL, HL
        Add HL to HL

        Flags affected:
        Z - not affected
        N - reset to 0
        H - Set if carry from bit 11
        C - Set if carry from bit 15
        :return:
        """
        data = (self.h << 8) | self.l
        return 8

    def _op_2a(self):
        """
        LD A, (HL+)
        Put value at address HL into register A. Increment HL afterwards.

        Flags affected:
        None
        :return:
        """
        self.a = self.mmu.read_byte((self.h << 8) + self.l)
        # TODO: INC (HL)
        return 8

    def _op_2b(self):
        """
        DEC HL
        Decrement register pair HL.

        Flags affected:
        None
        :return:
        """
        # DEC HL
        self.l = (self.l - 1) & 255
        if self.l == 255:
            self.h = (self.h - 1) & 255
        return 8

    def _op_2c(self):
        """
        INC L
        Increment register L.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('l')
        return 4

    def _op_2d(self):
        """
        DEC L
        Decrement register L.

        Flags affected:
        Z - Set if value is zero
        N - Set to 1
        H - Set if carry from bit 3
        C - Not affected
        :return:
        """
        self._dec('l')
        return 4

    def _op_2e(self):
        """
        LD L, d8
        Load next immediate byte value into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_2f(self):
        """
        CPL
        Complement A register. (Flip all bits)

        Flags affected:
        Z - Not affected
        N - Set to 1
        H - Set to 1
        C - Not affected
        :return:
        """
        self.a ^= 0xff
        self.sub_flag = 1
        self.hc_flag = 1
        return 4

    def _op_30(self):
        """
        JR NZ, nn
        If carry flag == 0 then add n to current address and jump to it.
        :return:
        """
        if self.carry_flag == 0:
            return self._op_18()
        else:
            self.pc += 1
            return 8

    def _op_31(self):
        """
        LD SP, d16
        Stack Pointer value becomes next two immediate byte values.

        Flags affected:
        None
        :return:
        """
        self.sp = self.mmu.read_word(self.pc)
        self.pc += 2
        return 12

    def _op_32(self):
        """
        LD (HL-), A
        Store value in register A into memory address HL. Decrement HL.

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.a)
        self.l = (self.l - 1) & 0xff
        if self.l == 255:
            self.h = (self.h - 1) & 0xff
        return 8

    def _op_33(self):
        """
        INC SP
        Increment Stack Pointer.

        Flags affected:
        None
        :return:
        """
        self.sp = (self.sp + 1) & 0xffff
        return 8

    def _op_34(self):
        """
        INC (HL)
        Increment value value stored at memory address (HL)

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry on bit 3
        C - Not affected
        :return:
        """
        addr = (self.h << 8) + self.l
        value = (self.mmu.read_byte(addr) + 1) & 0xff
        self.mmu.write_byte(addr, value)
        self.sub_flag = 0
        if value == 0:
            self.zero_flag = 1
        else:
            self.zero_flag = 0
        if (value & 0xf) == 0:
            self.hc_flag = 1
        else:
            self.hc_flag = 0
        return 12

    def _op_35(self):
        """
        DEC (HL)
        Decrement value stored at memory address (HL)

        Flags affected:
        Z - Set if value is zero
        N - Set to 1
        H - Set if carry on bit 3
        C - Not affected
        :return:
        """
        temp = self.mmu.read_byte((self.h << 8) + self.l)
        temp = (temp - 1) & 0xff
        self.mmu.write_byte((self.h << 8) + self.l, temp)
        self.zero_flag = 1 if temp == 0 else 0
        self.sub_flag = 1
        self.hc_flag = 1 if (temp & 0xf) > 0xf else 0
        return 12

    def _op_36(self):
        """
        LD (HL), d8
        Load next immediate byte value into memory address (HL)

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.pc)
        self.pc += 1
        # TODO: this may need to be updated. Will have to check whether it should be pc, or location in rom at pc
        return 12

    def _op_37(self):
        """
        SCF
        Set carry flag.

        Flags affected:
        Z - not affected
        N - set to zero
        H - set to zero
        C - set to 1
        :return:
        """
        self.carry_flag = 1
        self.hc_flag = 0
        self.sub_flag = 0
        return 4

    def _op_38(self):
        """
        JR NZ, nn
        If carr flag == 1 then add n to current address and jump to it.

        Flags affected:
        None
        :return:
        """
        if self.carry_flag:
            return self._op_18()
        else:
            self.pc += 1
            return 8

    def _op_39(self):
        """
        ADD HL, SP
        Adds stack pointer to register pair HL.

        Flags affected:
        Z - Not affected
        N - Reset to 0
        H - Set if carry from bit 11
        C - Set if carry from bit 15
        :return:
        """
        hl = (self.h << 8) + self.l
        if hl + self.sp > 0xffff:
            self.carry_flag |= 1
        if (hl & 0x0fff) + (self.sp & 0x0fff) > 0x0fff:
            self.hc_flag |= 1
        hl = (hl + self.sp) & 0xffff
        self.h = hl >> 8
        self.l = hl & 0xff
        return 8

    def _op_3a(self):
        """
        LD A, (HL-)
        Load value in memory address (HL) into register A. Decrement HL

        Flags affected:
        None
        :return:
        """
        self.a = self.mmu.read_byte((self.h << 8) + self.l)
        # TODO: DEC (HL)
        return 8

    def _op_3b(self):
        """
        DEC SP
        Decrement Stack pointer.

        Flags affected:
        None
        :return:
        """
        # DEC SP
        self.sp = (self.sp - 1) & 0xffff
        return 8

    def _op_3c(self):
        """
        INC A
        Increment register A.

        Flags affected:
        Z - Set if result is zero
        N - Reset
        H - Set if carry from bit 3.
        C - Not affected
        :return:
        """
        self._inc('a')
        return 4

    def _op_3d(self):
        """
        DEC A
        Decrement register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 1
        H - Set if carry on bit 3
        C - Not affected
        :return:
        """
        self._dec('a')
        return 4

    def _op_3e(self):
        """
        LD A, d8
        Load next immediate byte value into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.mmu.read_byte(self.pc)
        self.pc += 1
        return 8

    def _op_3f(self):
        """
        Complement carry flag.
        If C flag is set, then reset it.
        If C flag is reset, then set it.

        Flags affected:
        Z - no affected
        N - set to 0
        H - set to 0
        C - complemented
        :return:
        """
        self.sub_flag = 0
        self.hc_flag = 0
        self.carry_flag = 1 if self.carry_flag == 0 else 0
        return 4

    def _op_40(self):
        """
        LD B, B
        Load value in register B into register B. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_41(self):
        """
        LD B, C
        Load value in register C into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.c
        return 4

    def _op_42(self):
        """
        LD B, D
        Load value in register D into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.d
        return 4

    def _op_43(self):
        """
        LD B, E
        Load value in register E into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.e
        return 4

    def _op_44(self):
        """
        LD B, H
        Load value in register H into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.h
        return 4

    def _op_45(self):
        """
        LD B, L
        Load value in register L into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.l
        return 4

    def _op_46(self):
        """
        LD B, (HL)
        Load value stored in memory address (HL) into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.mmu.read_byte((self.h << 8) + self.l)
        return 8

    def _op_47(self):
        """
        LD B, A
        Load value in register A into register B.

        Flags affected:
        None
        :return:
        """
        self.b = self.a
        return 4

    def _op_48(self):
        """
        LD C, B
        Load value in register B into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.b
        return 4

    def _op_49(self):
        """
        LD C, C
        Load value in register C into register C. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_4a(self):
        """
        LD C, D
        Load value in register D into register C

        Flags affected:
        None
        :return:
        """
        self.c = self.d
        return 4

    def _op_4b(self):
        """
        LD C, E
        Load value in register E into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.e
        return 4

    def _op_4c(self):
        """
        LD C, H
        Load value in register H into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.h
        return 4

    def _op_4d(self):
        """
        LD C, L
        Load value in register L into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.l
        return 4

    def _op_4e(self):
        """
        LD C, (HL)
        Load value at memory address (HL) into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.mmu.read_byte((self.h << 8) + self.l)
        return 4

    def _op_4f(self):
        """
        LD C, A
        Load value in register A into register C.

        Flags affected:
        None
        :return:
        """
        self.c = self.a
        return 4

    def _op_50(self):
        """
        LD D, B
        Load value in register B into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.b
        return 4

    def _op_51(self):
        """
        LD D, C
        Load value in register C into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.c
        return 4

    def _op_52(self):
        """
        LD D, D
        Load value in register D into register D. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_53(self):
        """
        LD D, E
        Load value in register E into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.e
        return 4

    def _op_54(self):
        """
        LD D, H
        Load value in register H into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.h
        return 4

    def _op_55(self):
        """
        LD D, L
        Load value in register L into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.l
        return 4

    def _op_56(self):
        """
        LD D, (HL)
        Load value at memory address (HL) into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.mmu.read_byte(self.h << 8 + self.l)
        return 8

    def _op_57(self):
        """
        LD D, A
        Load value in register A into register D.

        Flags affected:
        None
        :return:
        """
        self.d = self.a
        return 4

    def _op_58(self):
        """
        LD E, B
        Load value in register B into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.b
        return 4

    def _op_59(self):
        """
        LD E, C
        Load value in register C into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.c
        return 4

    def _op_5a(self):
        """
        LD E, D
        Load value in register D into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.d
        return 4

    def _op_5b(self):
        """
        LD E, E
        Load value in register E into register E. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_5c(self):
        """
        LD E, H
        Load value in register H into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.h
        return 4

    def _op_5d(self):
        """
        LD E, L
        Load value in register L into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.l
        return 4

    def _op_5e(self):
        """
        LD E, (HL)
        Load value in register B into register B.

        Flags affected:
        None
        :return:
        """
        self.e = self.mmu.read_byte(self.h << 8 + self.l)
        return 8

    def _op_5f(self):
        """
        LD E, A
        Load value in register A into register E.

        Flags affected:
        None
        :return:
        """
        self.e = self.a
        return 4

    def _op_60(self):
        """
        LD H, B
        Load value in register B into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.b
        return 4

    def _op_61(self):
        """
        LD H, C
        Load value in register C into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.c
        return 4

    def _op_62(self):
        """
        LD H, D
        Load value in register D into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.d
        return 4

    def _op_63(self):
        """
        LD H, E
        Load value in register E into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.e
        return 4

    def _op_64(self):
        """
        LD H, H
        Load value in register H into register H. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_65(self):
        """
        LD H, L
        Load value in register L into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.l
        return 4

    def _op_66(self):
        """
        LD H, (HL)
        Load value at memory address (HL) into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.mmu.read_byte(self.h << 8 + self.l)
        return 8

    def _op_67(self):
        """
        LD H, A
        Load value in register A into register H.

        Flags affected:
        None
        :return:
        """
        self.h = self.a
        return 4

    def _op_68(self):
        """
        LD L, B
        Load value in register B into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.b
        return 4

    def _op_69(self):
        """
        LD L, C
        Load value in register C into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.c
        return 4

    def _op_6a(self):
        """
        LD L, D
        Load value in register D into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.d
        return 4

    def _op_6b(self):
        """
        LD L, E
        Load value in register E into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.e
        return 4

    def _op_6c(self):
        """
        LD L, H
        Load value in register H into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.h
        return 4

    def _op_6d(self):
        """
        LD L, L
        Load value in register L into register L. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_6e(self):
        """
        LD L, (HL)
        Load value at memory address (HL) into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.mmu.read_byte((self.h << 8) + self.l)
        return 8

    def _op_6f(self):
        """
        LD L, A
        Load value in register A into register L.

        Flags affected:
        None
        :return:
        """
        self.l = self.a
        return 4

    def _op_70(self):
        """
        LD (HL), B
        Load value in register B into memory address (HL).

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.b)
        return 8

    def _op_71(self):
        """
        LD (HL), C
        Load value in register C into memory address (HL)

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.c)
        return 8

    def _op_72(self):
        """
        LD (HL), D
        Load value in register D into memory address (HL)

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.d)
        return 8

    def _op_73(self):
        """
        LD (HL), E
        Load value in register E into memory address (HL).

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.e)
        return 8

    def _op_74(self):
        """
        LD (HL), H
        Load value in register H into memory address (HL).

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.h)
        return 8

    def _op_75(self):
        """
        LD (HL), L
        Load value in register L into memory address (HL)

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.l)
        return 8

    def _op_76(self):
        """
        HALT
        Halts cpu clock. Used in original GameBoy as a way to reduce energy consumption.
        Will wait until an interrupt occurs.

        Flags affected:
        None
        :return:
        """
        # TODO: Implement once we have started working on cycle routines
        return 4

    def _op_77(self):
        """
        LD (HL), A
        Load value in register A into memory address (HL).

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((self.h << 8) + self.l, self.a)
        return 8

    def _op_78(self):
        """
        LD A, B
        Load value in register B into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.b
        return 4

    def _op_79(self):
        """
        LD A, C
        Load value in register C into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.c
        return 4

    def _op_7a(self):
        """
        LD A, D
        Load value in register D into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.d
        return 4

    def _op_7b(self):
        """
        LD A, E
        Load value in register E into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.e
        return 4

    def _op_7c(self):
        """
        LD A, H
        Load value in register H into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.h
        return 4

    def _op_7d(self):
        """
        LD A, L
        Load value in register L into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.l
        return 4

    def _op_7e(self):
        """
        LD A, (HL)
        Load value at memory address (HL) into register A.

        Flags affected:
        None
        :return:
        """
        self.a = self.mmu.read_byte((self.h << 8) + self.l)
        return 8

    def _op_7f(self):
        """
        LD A, A
        Load value in register A into register A. Essentially treated as a NOP.

        Flags affected:
        None
        :return:
        """
        return 4

    def _op_80(self):
        """
        ADD A, B
        Adds values in registers A and B together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.b)
        return 4

    def _op_81(self):
        """
        ADD A, C
        Adds values in registers A and C together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.c)
        return 4

    def _op_82(self):
        """
        ADD A, D
        Adds values in registers A and D together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.d)
        return 4

    def _op_83(self):
        """
        ADD A, E
        Adds values in registers A and E together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.e)
        return 4

    def _op_84(self):
        """
        ADD A, H
        Adds values in registers A and H together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.h)
        return 4

    def _op_85(self):
        """
        ADD A, L
        Adds values in registers A and L together and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.l)
        return 4

    def _op_86(self):
        """
        ADD A, (HL)
        Adds value stored in memory address (HL) to regiter A and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_87(self):
        """
        ADD A, A
        Doubles value stored in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.a)
        return 4

    def _op_88(self):
        """
        ADC A, B
        Add register A and B with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.b + self.carry_flag)
        return 4

    def _op_89(self):
        """
        ADC A, C
        Add register A and C with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.c + self.carry_flag)
        return 4

    def _op_8a(self):
        """
        ADC A, D
        Add register A and D with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.d + self.carry_flag)
        return 4

    def _op_8b(self):
        """
        ADC A, E
        Add register A and E with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.e + self.carry_flag)
        return 4

    def _op_8c(self):
        """
        ADC A, H
        Add register A and H with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.h + self.carry_flag)
        return 4

    def _op_8d(self):
        """
        ADC A, L
        Add register A and L with carry bit and store value in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.l + self.carry_flag)
        return 4

    def _op_8e(self):
        """
        ADC A, (HL)
        Adds value stored in memory address (HL) to register A and carry flag and stores sum in register A.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.mmu.read_byte((self.h << 8) + self.l) + self.carry_flag)
        return 8

    def _op_8f(self):
        """
        ADC A, A
        Doubles register A and adds carry flag.

        Flags affected:
        Z - Set if value is zero
        N - Set to 0
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.a + self.carry_flag)
        return 4

    def _op_90(self):
        """
        SUB A, B
        Subtract value in register B from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.b)
        return 4

    def _op_91(self):
        """
        SUB A, C
        Subtract value in register C from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.c)
        return 4

    def _op_92(self):
        """
        SUB A, D
        Subtract value in register D from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.d)
        return 4

    def _op_93(self):
        """
        SUB A, E
        Subtract value in register E from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.e)
        return 4

    def _op_94(self):
        """
        SUB A, H
        Subtract value in register H from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.h)
        return 4

    def _op_95(self):
        """
        SUB A, L
        Subtract value in register L from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.l)
        return 4

    def _op_96(self):
        """
        SUB A, (HL)
        Subtract value stored at memory address (HL) from value in register A. Store remaining value in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_97(self):
        """
        SUB A, A
        Subtract register A from itself. Results in zero value every time.
        May not trip carry flags if value is low enough.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.a)
        return 4

    def _op_98(self):
        """
        SBC A, B
        Subtract register B from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.b + self.carry_flag)
        return 4

    def _op_99(self):
        """
        SBC A, C
        Subtract register C from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.c + self.carry_flag)
        return 4

    def _op_9a(self):
        """
        SBC A, D
        Subtract register D from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.d + self.carry_flag)
        return 4

    def _op_9b(self):
        """
        SBC A, E
        Subtract register E from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.e + self.carry_flag)
        return 4

    def _op_9c(self):
        """
        SBC A, H
        Subtract register H from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.h + self.carry_flag)
        return 4

    def _op_9d(self):
        """
        SBC A, L
        Subtract register L from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.l + self.carry_flag)
        return 4

    def _op_9e(self):
        """
        SBC A, (HL)
        Subtract value stored at memory address (HL) from register A and the carry flag.
        Store result in register A.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.mmu.read_byte((self.h << 8) + self.l) + self.carry_flag)
        return 8

    def _op_9f(self):
        """
        SBC A, A
        Subtract register A from register A and the carry flag.
        Depending on carry flag, this may or may not result in 0.

        Flags affected:
        Z - Set to 0
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.a + self.carry_flag)
        return 4

    def _op_a0(self):
        """
        AND B
        Logical bitwise AND the registers A and B, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.b)
        return 4

    def _op_a1(self):
        """
        AND C
        Logical bitwise AND the registers A and C, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.c)
        return 4

    def _op_a2(self):
        """
        AND D
        Logical bitwise AND the registers A and D, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.d)
        return 4

    def _op_a3(self):
        """
        AND E
        Logical bitwise AND the registers A and E, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.e)
        return 4

    def _op_a4(self):
        """
        AND H
        Logical bitwise AND the registers A and H, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.h)
        return 4

    def _op_a5(self):
        """
        AND L
        Logical bitwise AND the registers A and L, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.l)
        return 4

    def _op_a6(self):
        """
        AND (HL)
        Logical bitwise AND the value stored in memory at (HL) and the register A. Store the result in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_a7(self):
        """
        AND A
        Logical bitwise AND the registers A and A, store result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 1
        C - Set to 0
        :return:
        """
        self._and(self.a)
        return 4

    def _op_a8(self):
        """
        XOR B
        Logical bitwise XOR the registers A and B, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.b)
        return 4

    def _op_a9(self):
        """
        XOR C
        Logical bitwise XOR the registers A and C, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.c)
        return 4

    def _op_aa(self):
        """
        XOR D
        Logical bitwise XOR the registers A and D, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.d)
        return 4

    def _op_ab(self):
        """
        XOR E
        Logical bitwise XOR the registers A and E, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.e)
        return 4

    def _op_ac(self):
        """
        XOR H
        Logical bitwise XOR the registers A and H, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.h)
        return 4

    def _op_ad(self):
        """
        XOR L
        Logical bitwise XOR the registers A and L, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.l)
        return 4

    def _op_ae(self):
        """
        XOR (HL)
        Logical bitwise XOR the value stored in memory at address (HL) and register A. Store result in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_af(self):
        """
        XOR A
        Logical bitwise XOR the registers A and A, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._xor(self.a)
        return 4

    def _op_b0(self):
        """
        OR B
        Logical bitwise OR the registers A and B, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.b)
        return 4

    def _op_b1(self):
        """
        OR C
        Logical bitwise OR the registers A and C, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.c)
        return 4

    def _op_b2(self):
        """
        OR D
        Logical bitwise OR the registers A and D, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.d)
        return 4

    def _op_b3(self):
        """
        OR E
        Logical bitwise OR the registers A and E, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.e)
        return 4

    def _op_b4(self):
        """
        OR H
        Logical bitwise OR the registers A and H, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.h)
        return 4

    def _op_b5(self):
        """
        OR L
        Logical bitwise OR the registers A and L, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.l)
        return 4

    def _op_b6(self):
        """
        OR (HL)
        Logical bitwise OR the value stored in memory at address (HL) and register A. Store the result in register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_b7(self):
        """
        OR A
        Logical bitwise OR the registers A and A, store the result in A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 0
        H - Set to 0
        C - Set to 0
        :return:
        """
        self._or(self.a)
        return 4

    def _op_b8(self):
        """
        CP B
        Compare register B to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.b)
        return 4

    def _op_b9(self):
        """
        CP C
        Compare register C to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.c)
        return 4

    def _op_ba(self):
        """
        CP D
        Compare register D to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.d)
        return 4

    def _op_bb(self):
        """
        CP E
        Compare register E to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.e)
        return 4

    def _op_bc(self):
        """
        CP H
        Compare register H to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.h)
        return 4

    def _op_bd(self):
        """
        CP L
        Compare register L to register A. Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.l)
        return 4

    def _op_be(self):
        """
        CP (HL)
        Compare value stored in memory at (HL) with register A.
        Basically does a subtraction routine but does not store the result.
        Only flags are affected.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.mmu.read_byte((self.h << 8) + self.l))
        return 8

    def _op_bf(self):
        """
        CP A
        Compare register A to register A. Sets flags as seen below

        Flags affected:
        Z - 1
        N - 1
        H - 0
        C - 0
        :return:
        """
        self.zero_flag = 1
        self.sub_flag = 1
        self.hc_flag = 0
        self.carry_flag = 0
        return 4

    def _op_c0(self):
        """
        RET NZ
        Return if Zero flag is set to 0

        Flags affected:
        None
        :return:
        """
        if self.zero_flag == 0:
            return self._op_c9() + 4
        return 8

    def _op_c1(self):
        """
        POP BC
        Pop two bytes off stack into register pair BC. Increment Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.b = self.mmu.read_byte(self.sp + 1)
        self.c = self.mmu.read_byte(self.sp)
        self.sp = (self.sp + 2) & 0xffff
        return 12

    def _op_c2(self):
        """
        JP NZ, nn
        Jump to address nn if zero flag == 0

        Flags affected:
        None
        :return:
        """
        if self.zero_flag == 0:
            return self._op_c3()
        return 12

    def _op_c3(self):
        """
        JP nn
        Jump to address nn. nn is two next bytes read from memory at current program counter (pc)

        Flags affected:
        None
        :return:
        """
        self.pc = (self.mmu.read_byte(self.pc + 1) << 8) + self.mmu.read_byte(self.pc)
        return 16

    def _op_c4(self):
        """
        CALL NZ, nn
        Call address nn if Zero flag is set to 0.

        Flags affected:
        None
        :return:
        """
        if self.zero_flag == 0:
            return self._op_cd()
        return 12

    def _op_c5(self):
        """
        PUSH BC
        Push register pair BC onto stack.
        Decrement Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.sp = (self.sp - 2) & 0xffff
        self.mmu.write_byte(self.sp, self.c)
        self.mmu.write_byte(self.sp + 1, self.b)
        return 16

    def _op_c6(self):
        """
        ADD A, d8
        Add next value from pc in memory to register A.

        Flags affected:
        Z - Set if result is zero
        N - Reset to zero
        H - Set if carry from bit 3.
        C - Set if carry from bit 7.
        :return:
        """
        self._add(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_c7(self):
        """
        RST 0x00
        Push present address onto stack. (PC)
        Jump to address 0x0000

        Flags affected:
        None
        :return:
        """
        self._rst(0x0)
        return 16

    def _op_c8(self):
        """
        RET Z
        Return if Zero flag is set to 1

        Flags affected:
        None
        :return:
        """
        if self.zero_flag:
            return self._op_c9() + 4
        return 8

    def _op_c9(self):
        """
        RET
        Pop two bytes from stack and jump to that address.

        Flags affected:
        None
        :return:
        """
        low = self.mmu.read_byte(self.sp)
        high = self.mmu.read_byte(self.sp + 1)
        self.sp = (self.sp + 2) & 0xffff
        self.pc = (high << 8) | low
        return 16

    def _op_ca(self):
        """
        JP Z, nn
        Jump to address nn if zero flag == 1

        Flags affected:
        None
        :return:
        """
        if self.zero_flag:
            return self._op_c3()
        return 12

    def _op_cb(self):
        """
        Extended opcode table function.
        :return:
        """
        ext_op = self.ext_opcodes[self.mmu.read_byte(self.pc)]
        self.pc += 1
        return ext_op() + 4

    def _op_cc(self):
        """
        CALL Z,nn
        Call address nn if Zero flag is set to 1

        Flags affected:
        None
        :return:
        """
        if self.zero_flag:
            return self._op_cd()
        return 12

    def _op_cd(self):
        """
        CALL nn
        Push address of next instruction onto stack and then jump to address nn.

        Flags affected:
        None
        :return:
        """
        self.sp = (self.sp - 2) & 0xffff
        call_addr = self.mmu.read_byte(self.pc)
        call_addr += self.mmu.read_byte(self.pc + 1) << 8
        self.pc += 2
        self.mmu.write_byte(self.sp, self.pc & 0xff)
        self.mmu.write_byte(self.sp + 1, self.pc >> 8)
        self.pc = call_addr
        return 24

    def _op_ce(self):
        """
        ADC A, d8
        Add with carry next value in memory at pc to register A.

        Flags affected:
        Z - Set if result is zero
        N - Reset to zero
        H - Set if carry from bit 3
        C - Set if carry from bit 7
        :return:
        """
        self._add(self.mmu.read_byte(self.pc) + self.carry_flag)
        self.pc += 1
        return 8

    def _op_cf(self):
        """
        RST 0x8
        Push present address onto stack. (PC)
        Jump to address 0x0008

        Flags affected:
        None
        :return:
        """
        self._rst(0x8)
        return 16

    def _op_d0(self):
        """
        RET NC
        Return if Carr flag is set to 0

        Flags affected:
        None
        :return:
        """
        if self.carry_flag == 0:
            return self._op_c9() + 4
        return 8

    def _op_d1(self):
        """
        POP DE
        Pop two bytes off stack into register pair BC. Increment Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.d = self.mmu.read_byte(self.sp + 1)
        self.e = self.mmu.read_byte(self.sp)
        self.sp = (self.sp + 2) & 0xffff
        return 12

    def _op_d2(self):
        """
        JP NC, nn
        Jump to address nn if carry flag == 0

        Flags affected:
        None
        :return:
        """
        if self.carry_flag == 0:
            return self._op_c3()
        return 12

    def _op_d3(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_d4(self):
        """
        CALL NC, nn
        Call address nn if Carry flag is set to 0.

        Flags affected:
        None
        :return:
        """
        if self.carry_flag == 0:
            return self._op_cd()
        return 12

    def _op_d5(self):
        """
        PUSH DE
        Push register pair DE onto stack.
        Decrement Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.sp = (self.sp - 2) & 0xffff
        self.mmu.write_byte(self.sp, self.e)
        self.mmu.write_byte(self.sp + 1, self.d)
        return 16

    def _op_d6(self):
        """
        SUB A, d8
        Subtract next value in memory at pc from register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_d7(self):
        """
        RST 0x10
        Push present address onto stack. (PC)
        Jump to address 0x0010

        Flags affected:
        None
        :return:
        """
        self._rst(0x10)
        return 16

    def _op_d8(self):
        """
        RET C
        Return if Carry flag is set to 1

        Flags affected:
        None
        :return:
        """
        if self.carry_flag:
            return self._op_c9() + 4
        return 8

    def _op_d9(self):
        """
        RETI
        Return and enable interrupts.

        Flags affected:
        None
        :return:
        """
        self._op_c9()
        self.interrupts = True
        return 16

    def _op_da(self):
        """
        JP C, nn
        Jump to address nn if carry flag == 1

        Flags affected:
        None
        :return:
        """
        if self.carry_flag:
            return self._op_c3()
        return 12

    def _op_db(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_dc(self):
        """
        CALL C, nn
        Call address nn if Carry flag is set to 1.

        Flags affected:
        None
        :return:
        """
        if self.carry_flag:
            return self._op_cd()
        return 12

    def _op_dd(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_de(self):
        """
        SBC A, d8
        Subtract with carry next value in memory at pc from register A.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._sub(self.mmu.read_byte(self.pc) + self.carry_flag)
        self.pc += 1
        return 8

    def _op_df(self):
        """
        RST 0x18
        Push present address onto stack. (PC)
        Jump to address 0x0018

        Flags affected:
        None
        :return:
        """
        self._rst(0x18)
        return 16

    def _op_e0(self):
        """
        LDH (n), A
        Load A into memory address 0xff00 + n

        Flags affected:
        None
        :return:
        """
        offset = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.mmu.write_byte(0xff00 + offset, self.a)
        return 12

    def _op_e1(self):
        """
        POP HL
        Pop two bytes off stack into register pair BC. Increment Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.h = self.mmu.read_byte(self.sp + 1)
        self.l = self.mmu.read_byte(self.sp)
        self.sp = (self.sp + 2) & 0xffff
        return 12

    def _op_e2(self):
        """
        LD (C), A
        Put A into address 0xff00 + register C

        Flags affected:
        None
        :return:
        """
        self.mmu.write_byte((0xff00 + self.c), self.a)
        return 8

    def _op_e3(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_e4(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_e5(self):
        """
        PUSH HL
        Push register pair HL onto stack.
        Decrement Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        self.sp = (self.sp - 2) & 0xffff
        self.mmu.write_byte(self.sp, self.l)
        self.mmu.write_byte(self.sp + 1, self.h)
        return 16

    def _op_e6(self):
        """
        AND n
        Logically AND n with A, result in A.

        Flags affected:
        Z - set if result is zero
        N - reset to 0
        H - set to 0
        C - reset to 0
        :return:
        """
        self._and(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_e7(self):
        """
        RST 0x20
        Push present address onto stack.
        Jump to address 0x0020

        Flags affected:
        None
        :return:
        """
        self._rst(0x20)
        return 16

    def _op_e8(self):
        """
        ADD SP, n
        Add n to Stack Pointer (SP)

        Flags affected:
        Z - reset to 0
        N - reset to 0
        H - set or reset according to operation
        C - set or reset according to operation
        :return:
        """
        data = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.zero_flag = 0
        self.sub_flag = 0
        if (self.sp & 0xf) + (data & 0xf) > 0xf:
            self.hc_flag = 1
        else:
            self.hc_flag = 0
        if (self.sp & 0xff) + (data & 0xff) > 0xff:
            self.carry_flag = 1
        else:
            self.carry_flag = 0

        self.sp = (self.sp + data) & 0xffff
        return 16

    def _op_e9(self):
        """
        JP (HL)
        Jump to address contained in HL

        Flags affected:
        None
        :return:
        """
        self.pc = self.mmu.read_byte((self.h << 8) + self.l)
        return 4

    def _op_ea(self):
        """
        LD (nn), A
        Put value A into memory range given by next two bytes read from pc.

        Flags affected:
        None
        :return:
        """
        addr = self.mmu.read_byte(self.pc)
        self.pc += 1
        addr |= (self.mmu.read_byte(self.pc) << 8)
        self.pc += 1
        self.mmu.write_byte(addr, self.a)
        return 16

    def _op_eb(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_ec(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_ed(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_ee(self):
        """
        XOR d8
        Logical exclusive OR next value in memory at pc with register A, result in A.

        Flags affected:
        Z - Set if result is zero
        N - Reset to 0
        H - Reset to 0
        C - Reset to 0
        :return:
        """
        self._xor(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_ef(self):
        """
        RST 0x28
        Push present address onto stack.
        Jump to address 0x0028

        Flags affected:
        None
        :return:
        """
        self._rst(0x28)
        return 16

    def _op_f0(self):
        """
        LDH A, (a8)
        Load value stored in memory address 0xFF00 + n into register A.

        Flags affected:
        None
        :return:
        """
        offset = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.a = self.mmu.read_byte(0xff00 | offset)
        return 12

    def _op_f1(self):
        """
        POP AF
        Pop two bytes off stack into register A and flags register. Increment Stack Pointer (SP) twice.
        :return:
        """
        self.a = self.mmu.read_byte(self.sp + 1)
        self.f = self.mmu.read_byte(self.sp) & 0xf0  # flags only hold four bits here
        # TODO: need to translate this read into our separate flags
        self.sp = (self.sp + 2) & 0xffff
        return 12

    def _op_f2(self):
        """
        LD A, (C)
        Load value stored at memory address 0xFF00 + C into register A.

        Flags affected:
        None
        :return:
        """
        # LD A, (C)
        self.a = self.mmu.read_byte(0xff00 + self.c)
        return 8

    def _op_f3(self):
        """
        DI
        Disable Interrupts

        Flags affected:
        None
        :return:
        """
        self.interrupts = False
        return 4

    def _op_f4(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_f5(self):
        """
        PUSH AF
        Push register pair AF onto stack.
        Decrement Stack Pointer (SP) twice.

        Flags affected:
        None
        :return:
        """
        # TODO: need to find a way to implement pushing/popping flags register
        self.sp = (self.sp - 2) & 0xffff
        self.mmu.write_byte(self.sp, self.f)
        self.mmu.write_byte(self.sp + 1, self.a)
        return 16

    def _op_f6(self):
        """
        OR d8
        Logical OR next value in memory at pc with register A, result stored in A.

        Flags affected:
        Z - Set if result is 0
        N - Reset to 0
        H - Reset to 0
        C - Reset to 0
        :return:
        """
        self._or(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_f7(self):
        """
        RST 0x30
        Push present address onto stack.
        Jump to address 0x0030

        Flags affected:
        None
        :return:
        """
        self._rst(0x30)
        return 16

    def _op_f8(self):
        """
        LDHL SP, n
        Put Stack Pointer (SP) + n effective address into HL.

        Flags affected:
        Z - reset to 0
        N - reset to 0
        H - set or reset according to operation
        C - set or reset according to operation
        :return:
        """
        offset = self.mmu.read_byte(self.pc)
        self.pc += 1

        addr = self.sp + offset
        self.h = addr >> 8
        self.l = addr & 0xff
        self.zero_flag = 0
        self.sub_flag = 0
        if (self.sp & 0xf) + (offset & 0xf) > 0xf:
            self.hc_flag = 1
        else:
            self.hc_flag = 0
        if (self.sp & 0xff) + (offset & 0xff) > 0xff:
            self.carry_flag = 1
        else:
            self.carry_flag = 0
        return 12

    def _op_f9(self):
        """
        LD SP, HL
        Put HL into Stack Pointer (SP)

        Flags affected:
        None
        :return:
        """
        self.sp = (self.h << 8) | self.l
        return 8

    def _op_fa(self):
        """
        LD A, (a16)
        Store value at memory address given by next two read bytes into register A.

        Flags affected:
        None
        :return:
        """
        # LD A, (a16)
        self.a = self.mmu.read_word(self.pc)
        self.pc += 2
        return 16

    def _op_fb(self):
        """
        EI
        Enable interrupts, but not immediately. Interrupts are enabled after instruction after EI is executed.

        Flags affected:
        None
        :return:
        """
        # TODO: Need to wait one instruction then enable interrupts
        self.interrupts = True
        return 4

    def _op_fc(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_fd(self):
        """
        Not Implemented
        :return:
        """
        pass

    def _op_fe(self):
        """
        CP d8
        Compare A with next value in memory at pc. This is basically an A - n subtraction instruction but the results
        are thrown away.

        Flags affected:
        Z - Set if result is zero
        N - Set to 1
        H - Set if no borrow from bit 4
        C - Set if no borrow
        :return:
        """
        self._cp(self.mmu.read_byte(self.pc))
        self.pc += 1
        return 8

    def _op_ff(self):
        """
        RST 0x38
        Push present address onto stack.
        Jump to address 0x0038
        :return:
        """
        self._rst(0x38)
        return 16

    def _op_cb_00(self):
        pass

    def _op_cb_01(self):
        pass

    def _op_cb_02(self):
        pass

    def _op_cb_03(self):
        pass

    def _op_cb_04(self):
        pass

    def _op_cb_05(self):
        pass

    def _op_cb_06(self):
        pass

    def _op_cb_07(self):
        pass

    def _op_cb_08(self):
        pass

    def _op_cb_09(self):
        pass

    def _op_cb_0a(self):
        pass

    def _op_cb_0b(self):
        pass

    def _op_cb_0c(self):
        pass

    def _op_cb_0d(self):
        pass

    def _op_cb_0e(self):
        pass

    def _op_cb_0f(self):
        pass

    def _op_cb_10(self):
        pass

    def _op_cb_11(self):
        """
        RL C
        Rotate C left through Carry flag.

        Flags affected:
        Z - Set if result is zero
        N - Reset to 0
        H - Reset to 0
        C - Contains old bit 7 data
        :return:
        """
        self.sub_flag = 0
        self.hc_flag = 0
        self.carry_flag = (self.c & 0x80) >> 7
        self.c = (self.c << 1) & 0xff
        if self.c == 0:
            self.zero_flag = 1

    def _op_cb_12(self):
        pass

    def _op_cb_13(self):
        pass

    def _op_cb_14(self):
        pass

    def _op_cb_15(self):
        pass

    def _op_cb_16(self):
        pass

    def _op_cb_17(self):
        pass

    def _op_cb_18(self):
        pass

    def _op_cb_19(self):
        pass

    def _op_cb_1a(self):
        pass

    def _op_cb_1b(self):
        pass

    def _op_cb_1c(self):
        pass

    def _op_cb_1d(self):
        pass

    def _op_cb_1e(self):
        pass

    def _op_cb_1f(self):
        pass

    def _op_cb_20(self):
        pass

    def _op_cb_21(self):
        pass

    def _op_cb_22(self):
        pass

    def _op_cb_23(self):
        pass

    def _op_cb_24(self):
        pass

    def _op_cb_25(self):
        pass

    def _op_cb_26(self):
        pass

    def _op_cb_27(self):
        pass

    def _op_cb_28(self):
        pass

    def _op_cb_29(self):
        pass

    def _op_cb_2a(self):
        pass

    def _op_cb_2b(self):
        pass

    def _op_cb_2c(self):
        pass

    def _op_cb_2d(self):
        pass

    def _op_cb_2e(self):
        pass

    def _op_cb_2f(self):
        pass

    def _op_cb_30(self):
        pass

    def _op_cb_31(self):
        pass

    def _op_cb_32(self):
        pass

    def _op_cb_33(self):
        pass

    def _op_cb_34(self):
        pass

    def _op_cb_35(self):
        pass

    def _op_cb_36(self):
        pass

    def _op_cb_37(self):
        pass

    def _op_cb_38(self):
        pass

    def _op_cb_39(self):
        pass

    def _op_cb_3a(self):
        pass

    def _op_cb_3b(self):
        pass

    def _op_cb_3c(self):
        pass

    def _op_cb_3d(self):
        pass

    def _op_cb_3e(self):
        pass

    def _op_cb_3f(self):
        pass

    def _op_cb_40(self):
        pass

    def _op_cb_41(self):
        pass

    def _op_cb_42(self):
        pass

    def _op_cb_43(self):
        pass

    def _op_cb_44(self):
        pass

    def _op_cb_45(self):
        pass

    def _op_cb_46(self):
        pass

    def _op_cb_47(self):
        pass

    def _op_cb_48(self):
        pass

    def _op_cb_49(self):
        pass

    def _op_cb_4a(self):
        pass

    def _op_cb_4b(self):
        pass

    def _op_cb_4c(self):
        pass

    def _op_cb_4d(self):
        pass

    def _op_cb_4e(self):
        pass

    def _op_cb_4f(self):
        pass

    def _op_cb_50(self):
        pass

    def _op_cb_51(self):
        pass

    def _op_cb_52(self):
        pass

    def _op_cb_53(self):
        pass

    def _op_cb_54(self):
        pass

    def _op_cb_55(self):
        pass

    def _op_cb_56(self):
        pass

    def _op_cb_57(self):
        pass

    def _op_cb_58(self):
        pass

    def _op_cb_59(self):
        pass

    def _op_cb_5a(self):
        pass

    def _op_cb_5b(self):
        pass

    def _op_cb_5c(self):
        pass

    def _op_cb_5d(self):
        pass

    def _op_cb_5e(self):
        pass

    def _op_cb_5f(self):
        pass

    def _op_cb_60(self):
        pass

    def _op_cb_61(self):
        pass

    def _op_cb_62(self):
        pass

    def _op_cb_63(self):
        pass

    def _op_cb_64(self):
        pass

    def _op_cb_65(self):
        pass

    def _op_cb_66(self):
        pass

    def _op_cb_67(self):
        pass

    def _op_cb_68(self):
        pass

    def _op_cb_69(self):
        pass

    def _op_cb_6a(self):
        pass

    def _op_cb_6b(self):
        pass

    def _op_cb_6c(self):
        pass

    def _op_cb_6d(self):
        pass

    def _op_cb_6e(self):
        pass

    def _op_cb_6f(self):
        pass

    def _op_cb_70(self):
        pass

    def _op_cb_71(self):
        pass

    def _op_cb_72(self):
        pass

    def _op_cb_73(self):
        pass

    def _op_cb_74(self):
        pass

    def _op_cb_75(self):
        pass

    def _op_cb_76(self):
        pass

    def _op_cb_77(self):
        pass

    def _op_cb_78(self):
        pass

    def _op_cb_79(self):
        pass

    def _op_cb_7a(self):
        pass

    def _op_cb_7b(self):
        pass

    def _op_cb_7c(self):
        """
        BIT 7, H
        Test bit 7 in register H.

        Flags affected:
        Z - Set if bit 7 of register H is 0
        N - Reset to 0
        H - Set to 1
        C - Not affected
        :return:
        """
        self.sub_flag = 0
        self.hc_flag = 1
        if self.h & 0x80 == 0x80:
            self.zero_flag = 0
        else:
            self.zero_flag = 1

    def _op_cb_7d(self):
        pass

    def _op_cb_7e(self):
        pass

    def _op_cb_7f(self):
        pass

    def _op_cb_80(self):
        pass

    def _op_cb_81(self):
        pass

    def _op_cb_82(self):
        pass

    def _op_cb_83(self):
        pass

    def _op_cb_84(self):
        pass

    def _op_cb_85(self):
        pass

    def _op_cb_86(self):
        pass

    def _op_cb_87(self):
        pass

    def _op_cb_88(self):
        pass

    def _op_cb_89(self):
        pass

    def _op_cb_8a(self):
        pass

    def _op_cb_8b(self):
        pass

    def _op_cb_8c(self):
        pass

    def _op_cb_8d(self):
        pass

    def _op_cb_8e(self):
        pass

    def _op_cb_8f(self):
        pass

    def _op_cb_90(self):
        pass

    def _op_cb_91(self):
        pass

    def _op_cb_92(self):
        pass

    def _op_cb_93(self):
        pass

    def _op_cb_94(self):
        pass

    def _op_cb_95(self):
        pass

    def _op_cb_96(self):
        pass

    def _op_cb_97(self):
        pass

    def _op_cb_98(self):
        pass

    def _op_cb_99(self):
        pass

    def _op_cb_9a(self):
        pass

    def _op_cb_9b(self):
        pass

    def _op_cb_9c(self):
        pass

    def _op_cb_9d(self):
        pass

    def _op_cb_9e(self):
        pass

    def _op_cb_9f(self):
        pass

    def _op_cb_a0(self):
        pass

    def _op_cb_a1(self):
        pass

    def _op_cb_a2(self):
        pass

    def _op_cb_a3(self):
        pass

    def _op_cb_a4(self):
        pass

    def _op_cb_a5(self):
        pass

    def _op_cb_a6(self):
        pass

    def _op_cb_a7(self):
        pass

    def _op_cb_a8(self):
        pass

    def _op_cb_a9(self):
        pass

    def _op_cb_aa(self):
        pass

    def _op_cb_ab(self):
        pass

    def _op_cb_ac(self):
        pass

    def _op_cb_ad(self):
        pass

    def _op_cb_ae(self):
        pass

    def _op_cb_af(self):
        pass

    def _op_cb_b0(self):
        pass

    def _op_cb_b1(self):
        pass

    def _op_cb_b2(self):
        pass

    def _op_cb_b3(self):
        pass

    def _op_cb_b4(self):
        pass

    def _op_cb_b5(self):
        pass

    def _op_cb_b6(self):
        pass

    def _op_cb_b7(self):
        pass

    def _op_cb_b8(self):
        pass

    def _op_cb_b9(self):
        pass

    def _op_cb_ba(self):
        pass

    def _op_cb_bb(self):
        pass

    def _op_cb_bc(self):
        pass

    def _op_cb_bd(self):
        pass

    def _op_cb_be(self):
        pass

    def _op_cb_bf(self):
        pass

    def _op_cb_c0(self):
        pass

    def _op_cb_c1(self):
        pass

    def _op_cb_c2(self):
        pass

    def _op_cb_c3(self):
        pass

    def _op_cb_c4(self):
        pass

    def _op_cb_c5(self):
        pass

    def _op_cb_c6(self):
        pass

    def _op_cb_c7(self):
        pass

    def _op_cb_c8(self):
        pass

    def _op_cb_c9(self):
        pass

    def _op_cb_ca(self):
        pass

    def _op_cb_cb(self):
        pass

    def _op_cb_cc(self):
        pass

    def _op_cb_cd(self):
        pass

    def _op_cb_ce(self):
        pass

    def _op_cb_cf(self):
        pass

    def _op_cb_d0(self):
        pass

    def _op_cb_d1(self):
        pass

    def _op_cb_d2(self):
        pass

    def _op_cb_d3(self):
        pass

    def _op_cb_d4(self):
        pass

    def _op_cb_d5(self):
        pass

    def _op_cb_d6(self):
        pass

    def _op_cb_d7(self):
        pass

    def _op_cb_d8(self):
        pass

    def _op_cb_d9(self):
        pass

    def _op_cb_da(self):
        pass

    def _op_cb_db(self):
        pass

    def _op_cb_dc(self):
        pass

    def _op_cb_dd(self):
        pass

    def _op_cb_de(self):
        pass

    def _op_cb_df(self):
        pass

    def _op_cb_e0(self):
        pass

    def _op_cb_e1(self):
        pass

    def _op_cb_e2(self):
        pass

    def _op_cb_e3(self):
        pass

    def _op_cb_e4(self):
        pass

    def _op_cb_e5(self):
        pass

    def _op_cb_e6(self):
        pass

    def _op_cb_e7(self):
        pass

    def _op_cb_e8(self):
        pass

    def _op_cb_e9(self):
        pass

    def _op_cb_ea(self):
        pass

    def _op_cb_eb(self):
        pass

    def _op_cb_ec(self):
        pass

    def _op_cb_ed(self):
        pass

    def _op_cb_ee(self):
        pass

    def _op_cb_ef(self):
        pass

    def _op_cb_f0(self):
        pass

    def _op_cb_f1(self):
        pass

    def _op_cb_f2(self):
        pass

    def _op_cb_f3(self):
        pass

    def _op_cb_f4(self):
        pass

    def _op_cb_f5(self):
        pass

    def _op_cb_f6(self):
        pass

    def _op_cb_f7(self):
        pass

    def _op_cb_f8(self):
        pass

    def _op_cb_f9(self):
        pass

    def _op_cb_fa(self):
        pass

    def _op_cb_fb(self):
        pass

    def _op_cb_fc(self):
        pass

    def _op_cb_fd(self):
        pass

    def _op_cb_fe(self):
        pass

    def _op_cb_ff(self):
        pass
