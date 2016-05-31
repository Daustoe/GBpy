from gbpy.mmu import MMU
__author__ = 'Clayton Powell'


class Cpu(object):
    """
    Cpu class that emulates the GameBoy cpu for the emulator.
    """

    def __init__(self):
        self.pc = 0  # Program Counter
        self.previous_pc = 0
        self.sp = 0  # Stack Pointer
        self.mmu = MMU()  # Memory Management Unit
        self.opcode = 0

        # Registers
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0

        # clock values
        self.m = 0
        self.t = 0
        self.clock = {'m': self.m, 't': self.t}

        # we keep the flags separate instead of in the f register. No need to complicate this process.
        self.zero_flag = 0     # 0x80
        self.sub_flag = 0      # 0x40
        self.hc_flag = 0       # 0x20
        self.carry_flag = 0    # 0x10

        # Opcode map
        self.opcodes = {
            0x00: self._nop(),
            0x01: self._op_01(),
            0x02: self._op_02(),
            0x03: self._op_03(),
            0x04: self._op_03(),
            0x05: self._op_05(),
            0x06: self._op_06(),
            0x07: self._op_07(),
            0x08: self._op_08(),
            0x09: self._op_09(),
            0x0a: self._op_0a(),
            0x0b: self._op_0b(),
            0x0c: self._op_0c(),
            0x0d: None,
            0x0e: None,
            0x0f: None,
            0x10: None,
            0x11: None,
            0x12: None,
            0x13: None,
            0x14: None,
            0x15: None,
            0x16: None,
            0x17: None,
            0x18: None,
            0x19: None,
            0x1a: None,
            0x1b: None,
            0x1c: None,
            0x1d: None,
            0x1e: None,
            0x1f: None,
            0x20: None,
            0x21: None,
            0x22: None,
            0x23: None,
            0x24: None,
            0x25: None,
            0x26: None,
            0x27: None,
            0x28: None,
            0x29: None,
            0x2a: None,
            0x2b: None,
            0x2c: None,
            0x2d: None,
            0x2e: None,
            0x2f: None,
            0x30: None,
            0x31: None,
            0x32: None,
            0x33: None,
            0x34: None,
            0x35: None,
            0x36: None,
            0x37: None,
            0x38: None,
            0x39: None,
            0x3a: None,
            0x3b: None,
            0x3c: None,
            0x3d: None,
            0x3e: None,
            0x3f: None,
            0x40: self._ld(self.b, self.b),
            0x41: self._ld(self.b, self.c),
            0x42: self._ld(self.b, self.d),
            0x43: self._ld(self.b, self.e),
            0x44: self._ld(self.b, self.h),
            0x45: self._ld(self.b, self.l),
            0x46: None,  # TODO: LD B, (HL)
            0x47: self._ld(self.b, self.a),
            0x48: self._ld(self.c, self.b),
            0x49: self._ld(self.c, self.c),
            0x4a: self._ld(self.c, self.d),
            0x4b: self._ld(self.c, self.e),
            0x4c: self._ld(self.c, self.h),
            0x4d: self._ld(self.c, self.l),
            0x4e: None,  # TODO: LD C, (HL)
            0x4f: self._ld(self.c, self.a),
            0x50: self._ld(self.d, self.b),
            0x51: self._ld(self.d, self.c),
            0x52: self._ld(self.d, self.d),
            0x53: self._ld(self.d, self.e),
            0x54: self._ld(self.d, self.h),
            0x55: self._ld(self.d, self.l),
            0x56: None,  # TODO: LD D, (HL)
            0x57: self._ld(self.d, self.a),
            0x58: self._ld(self.e, self.b),
            0x59: self._ld(self.e, self.c),
            0x5a: self._ld(self.e, self.d),
            0x5b: self._ld(self.e, self.e),
            0x5c: self._ld(self.e, self.h),
            0x5d: self._ld(self.e, self.l),
            0x5e: None,  # TODO: LD E, (HL)
            0x5f: self._ld(self.e, self.a),
            0x60: self._ld(self.h, self.b),
            0x61: self._ld(self.h, self.c),
            0x62: self._ld(self.h, self.d),
            0x63: self._ld(self.h, self.e),
            0x64: self._ld(self.h, self.h),
            0x65: self._ld(self.h, self.l),
            0x66: None,  # TODO: LD H, (HL)
            0x67: self._ld(self.h, self.a),
            0x68: self._ld(self.l, self.b),
            0x69: self._ld(self.l, self.c),
            0x6a: self._ld(self.l, self.d),
            0x6b: self._ld(self.l, self.e),
            0x6c: self._ld(self.l, self.h),
            0x6d: self._ld(self.l, self.l),
            0x6e: None,  # TODO: LD L, (HL)
            0x6f: self._ld(self.l, self.a),
            0x70: None,  # TODO: LD (HL), B
            0x71: None,  # TODO: LD (HL), C
            0x72: None,  # TODO: LD (HL), D
            0x73: None,  # TODO: LD (HL), E
            0x74: None,  # TODO: LD (HL), H
            0x75: None,  # TODO: LD (HL), L
            0x76: self._halt(),
            0x77: None,  # TODO: LD (HL), A
            0x78: self._ld(self.a, self.b),
            0x79: self._ld(self.a, self.c),
            0x7a: self._ld(self.a, self.d),
            0x7b: self._ld(self.a, self.e),
            0x7c: self._ld(self.a, self.h),
            0x7d: self._ld(self.a, self.l),
            0x7e: None,  # TODO: LD A, (HL)
            0x7f: self._ld(self.a, self.a),
            0x80: self._add(self.b),
            0x81: self._add(self.c),
            0x82: self._add(self.d),
            0x83: self._add(self.e),
            0x84: self._add(self.h),
            0x85: self._add(self.l),
            0x86: None,  # TODO: ADD (HL)
            0x87: self._add(self.a),
            0x88: self._adc(self.b),
            0x89: self._adc(self.c),
            0x8a: self._adc(self.d),
            0x8b: self._adc(self.e),
            0x8c: self._adc(self.h),
            0x8d: self._adc(self.l),
            0x8e: None,  # TODO: ADC (HL)
            0x8f: self._adc(self.a),
            0x90: self._sub(self.b),
            0x91: self._sub(self.c),
            0x92: self._sub(self.d),
            0x93: self._sub(self.e),
            0x94: self._sub(self.h),
            0x95: self._sub(self.l),
            0x96: None,  # TODO: SUB (HL)
            0x97: self._sub(self.a),
            0x98: self._sbc(self.b),
            0x99: self._sbc(self.c),
            0x9a: self._sbc(self.d),
            0x9b: self._sbc(self.e),
            0x9c: self._sbc(self.h),
            0x9d: self._sbc(self.l),
            0x9e: None,  # TODO: SBC (HL)
            0x9f: self._sbc(self.a),
            0xa0: self._and(self.b),
            0xa1: self._and(self.c),
            0xa2: self._and(self.d),
            0xa3: self._and(self.e),
            0xa4: self._and(self.h),
            0xa5: self._and(self.l),
            0xa6: None,  # TODO: AND (HL)
            0xa7: self._and(self.a),
            0xa8: self._xor(self.b),
            0xa9: self._xor(self.c),
            0xaa: self._xor(self.d),
            0xab: self._xor(self.e),
            0xac: self._xor(self.h),
            0xad: self._xor(self.l),
            0xae: None,  # TODO: XOR (HL)
            0xaf: self._xor(self.a),
            0xb0: self._or(self.b),
            0xb1: self._or(self.c),
            0xb2: self._or(self.d),
            0xb3: self._or(self.e),
            0xb4: self._or(self.h),
            0xb5: self._or(self.l),
            0xb6: None,  # TODO: OR (HL)
            0xb7: self._or(self.a),
            0xb8: None,
            0xb9: None,
            0xba: None,
            0xbb: None,
            0xbc: None,
            0xbd: None,
            0xbe: None,
            0xbf: None,
            0xc0: None,
            0xc1: None,
            0xc2: None,
            0xc3: None,
            0xc4: None,
            0xc5: None,
            0xc6: None,
            0xc7: self._rst(0x00),
            0xc8: None,
            0xc9: None,
            0xca: None,
            0xcb: None,
            0xcc: None,
            0xcd: None,
            0xce: None,
            0xcf: self._rst(0x08),
            0xd0: None,
            0xd1: None,
            0xd2: None,
            0xd3: None,
            0xd4: None,
            0xd5: None,
            0xd6: None,
            0xd7: self._rst(0x10),
            0xd8: None,
            0xd9: None,
            0xda: None,
            0xdb: None,
            0xdc: None,
            0xdd: None,
            0xde: None,
            0xdf: self._rst(0x18),
            0xe0: None,
            0xe1: None,
            0xe2: None,
            0xe3: None,
            0xe4: None,
            0xe5: None,
            0xe6: None,
            0xe7: self._rst(0x20),
            0xe8: None,
            0xe9: None,
            0xea: None,
            0xeb: None,
            0xec: None,
            0xed: None,
            0xee: None,
            0xef: self._rst(0x28),
            0xf0: None,
            0xf1: None,
            0xf2: None,
            0xf3: None,
            0xf4: None,
            0xf5: None,
            0xf6: None,
            0xf7: self._rst(0x30),
            0xf8: None,
            0xf9: None,
            0xfa: None,
            0xfb: None,
            0xfc: None,
            0xfd: None,
            0xfe: None,
            0xff: self._rst(0x38),
        }
        # TODO: Implement extended operations
        self.ext_opcodes = {}

    def cycle(self):
        """
        Single cpu cycle. Reads opcode at program counter in memory. Executes that opcode.
        """
        self.previous_pc = self.pc
        self.opcode = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.opcodes[self.opcode]()
        self.pc &= 0xffff
        self.clock['m'] = self.m

    def _nop(self):
        """
        No operation, idle cycle
        :return:
        """
        self.m = 1

    def _halt(self):
        """

        :return:
        """
        pass

    def _rst(self, pc):
        """
        Push present program counter (pc) onto stack. Jump to new pc given.
        :param pc:
        :return:
        """
        # TODO: Need to push pc to stack before we set pc to new value.
        self.pc = pc
        self.m = 3

    def _ld(self, storage, value):
        """
        Store value into 'storage' register.

        Flags affected:
        --None--

        :param storage:
        :param value:
        :return:
        """
        # TODO: Implement
        pass

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
        # Add register A to given register and store in A. Check for flags.
        self.hc_flag = 1 if (self.a & 0xf) + (value & 0xf) > 0xf else 0
        self.a += value
        self.carry_flag = 1 if self.a > 0xff else 0
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0
        self.sub_flag = 0
        self.m = 1

    def _adc(self, value):
        # Add with carry.
        """
        var a=Z80._r.a;
        Z80._r.a+=Z80._r.b;
        Z80._r.a+=(Z80._r.f&0x10)?1:0;
        Z80._r.f=(Z80._r.a>255)?0x10:0;
        Z80._r.a&=255;
        if(!Z80._r.a) Z80._r.f|=0x80;
        if((Z80._r.a^Z80._r.b^a)&0x10) Z80._r.f|=0x20;
        Z80._r.m=1;

        :param value:
        :return:
        """
        pass

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
        # TODO: Implement
        pass

    def _sbc(self, value):
        """
        Subtract value + Carry flag from register A.

        Flags affected:
        Z - Set if result is zero
        N - Set
        H - Set if no borrow from bit 4
        C - Set if no borrow

        :param value:
        :return:
        """
        # TODO: Implement
        pass

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
        self.m = 1

    def _or(self, value):
        # Logical OR command, takes a register as an argument and or's it with register A
        self.a |= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0  # z_flag will be 1 if self.a == 0, else z_flag will be 0
        self.carry_flag = 0
        self.hc_flag = 0
        self.sub_flag = 0
        self.m = 1

    def _xor(self, value):
        # Logical XOR command, takes a register as an argument and xor's it with register A
        self.a ^= value
        self.a &= 0xff
        self.zero_flag = 1 if self.a == 0 else 0  # z_flag will be 1 if self.a == 0, else z_flag will be 0
        self.carry_flag = 0
        self.hc_flag = 0
        self.sub_flag = 0
        self.m = 1

    def _op_01(self):
        # LD BC, d16
        self.c = self.mmu.read_byte(self.pc)
        self.b = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        self.m = 3

    def _op_02(self):
        # LD (BC), A
        self.mmu.write_byte((self.b << 8) + self.c, self.a)
        self.m = 2

    def _op_03(self):
        # INC BC
        self.c = (self.c + 1) & 0xff
        if self.c == 0:
            self.b = (self.b + 1) & 0xff
        self.m = 1

    def _op_04(self):
        # INC B
        self.b = (self.b + 1) & 0xff
        self.sub_flag = 0
        if self.b == 0:
            self.zero_flag |= 1
        if self.b & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_05(self):
        # DEC B
        self.b = (self.b - 1) & 0xff
        self.sub_flag = 1
        if self.b == 0:
            self.zero_flag |= 1
        if self.b & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_06(self):
        # LD B, d8
        self.b = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_07(self):
        # RLCA
        high_bit = (self.a & 0x80) / 0x80
        self.a = ((self.a << 1) & 0xff) | high_bit
        self.carry_flag = high_bit
        self.m = 1

    def _op_08(self):
        # LD (a16), SP          (may need work)
        self.mmu.write_word(self.pc, self.sp)
        self.m = 4

    def _op_09(self):
        # ADD HL, BC
        hl = (self.h << 8) + self.l
        bc = (self.b << 8) + self.c
        # may need to do something with Zero flag here
        if hl + bc > 0xffff:
            self.carry_flag |= 1
        if (hl & 0x0fff) + (bc & 0x0fff) > 0x0fff:
            self.hc_flag |= 1
        hl = (hl + bc) & 0xffff
        self.h = hl >> 8
        self.l = hl & 0xff
        self.m = 3

    def _op_0a(self):
        # LD A, (BC)
        self.a = self.mmu.read_byte((self.b << 8) | self.c)
        self.m = 2

    def _op_0b(self):
        # DEC BC
        self.c = (self.c - 1) & 0xff
        if self.c == 0xff:
            self.b = (self.b - 1) & 0xff
        self.m = 1

    def _op_0c(self):
        # INC C
        self.c = (self.c + 1) & 0xff
        self.sub_flag = 0
        if self.c == 0:
            self.zero_flag |= 1
        if self.c & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_0d(self):
        # DEC C
        self.c = (self.c - 1) & 0xff
        self.sub_flag = 1
        if self.c == 0:
            self.zero_flag |= 1
        if self.c & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_0e(self):
        # LD C, d8
        self.c = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_0f(self):
        # RRCA
        pass

    def _op_10(self):
        # STOP 0
        pass

    def _op_11(self):
        # LD DE, d16
        self.d = self.mmu.read_byte(self.pc)
        self.e = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        self.m = 3

    def _op_12(self):
        # LD (DE), A
        self.mmu.write_byte((self.d << 8) + self.e, self.a)
        self.m = 2

    def _op_13(self):
        # INC DE
        self.e = (self.e + 1) & 0xff
        if self.e == 0:
            self.d = (self.d + 1) & 0xff
        self.m = 1

    def _op_14(self):
        # INC D
        self.d = (self.d + 1) & 0xff
        self.sub_flag = 0
        if self.d == 0:
            self.zero_flag |= 1
        if self.d & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_15(self):
        # DEC D
        self.d = (self.d - 1) & 0xff
        self.sub_flag = 1
        if self.d == 0:
            self.zero_flag |= 1
        if self.d & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_16(self):
        # LD D, d8
        self.d = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_17(self):
        # RLA
        pass

    def _op_18(self):
        # JR r8
        pass

    def _op_19(self):
        # ADD HL, DE
        pass

    def _op_1a(self):
        # LD A, (DE)
        self.a = self.mmu.read_byte((self.d << 8) | self.e)
        self.m = 2

    def _op_1b(self):
        # DEC DE
        pass

    def _op_1c(self):
        # INC E
        self.e = (self.e + 1) & 0xff
        self.sub_flag = 0
        if self.e == 0:
            self.zero_flag |= 1
        if self.e & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_1d(self):
        # DEC E
        self.e = (self.e - 1) & 0xff
        self.sub_flag = 1
        if self.e == 0:
            self.zero_flag |= 1
        if self.e & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_1e(self):
        # LD E, d8
        self.e = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_1f(self):
        # RRA
        pass

    def _op_20(self):
        # JR NZ, r8
        pass

    def _op_21(self):
        # LD HL, d16
        self.h = self.mmu.read_byte(self.pc)
        self.l = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        self.m = 3

    def _op_22(self):
        # LD (HL+), A
        pass

    def _op_23(self):
        # INC HL
        self.l = (self.l + 1) & 0xff
        if self.e == 0:
            self.h = (self.h + 1) & 0xff
        self.m = 1

    def _op_24(self):
        # INC H
        self.h = (self.h + 1) & 0xff
        self.sub_flag = 0
        if self.h == 0:
            self.zero_flag |= 1
        if self.h & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_25(self):
        # DEC H
        self.h = (self.h - 1) & 0xff
        self.sub_flag = 1
        if self.h == 0:
            self.zero_flag |= 1
        if self.h & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_26(self):
        # LD H, d8
        self.h = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_27(self):
        # DAA
        pass

    def _op_28(self):
        # JR Z, r8
        pass

    def _op_29(self):
        # ADD HL, HL
        pass

    def _op_2a(self):
        # LD A, (HL+)
        pass

    def _op_2b(self):
        # DEC HL
        pass

    def _op_2c(self):
        # INC L
        self.l = (self.l + 1) & 0xff
        self.sub_flag = 0
        if self.l == 0:
            self.zero_flag |= 1
        if self.l & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_2d(self):
        # DEC L
        self.l = (self.l - 1) & 0xff
        self.sub_flag = 1
        if self.l == 0:
            self.zero_flag |= 1
        if self.l & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_2e(self):
        # LD L, d8
        self.l = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_2f(self):
        # CPL
        self.a ^= 0xff
        # some flags to check here?
        self.m = 1

    def _op_30(self):
        # JR NC, r8
        pass

    def _op_31(self):
        # LD SP, d16
        self.sp = self.mmu.read_word(self.pc)
        self.pc += 2
        self.m = 3

    def _op_32(self):
        # LD (HL-), A
        pass

    def _op_33(self):
        # INC SP
        self.sp = (self.sp + 1) & 0xffff
        self.m = 1

    def _op_34(self):
        # INC (HL)
        # Increment value stored at memory address (HL)
        # self.mmu.read_byte()
        pass

    def _op_35(self):
        # DEC (HL)
        # Decrement value stored at memory address (HL)
        pass

    def _op_36(self):
        # LD (HL), d8
        # Load byte value into memory address (HL)
        pass

    def _op_37(self):
        # SCF
        pass

    def _op_38(self):
        # JR C, r8
        pass

    def _op_39(self):
        # ADD HL, SP
        pass

    def _op_3a(self):
        # LD A, (HL-)
        pass

    def _op_3b(self):
        # DEC SP
        self.sp = (self.sp - 1) & 0xffff
        self.m = 1

    def _op_3c(self):
        # INC A
        self.a = (self.a + 1) & 0xff
        self.sub_flag = 0
        if self.a == 0:
            self.zero_flag |= 1
        if self.a & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_3d(self):
        # DEC A
        self.a = (self.a - 1) & 0xff
        self.sub_flag = 1
        if self.a == 0:
            self.zero_flag |= 1
        if self.a & 0xf == 0:
            self.hc_flag |= 1
        self.m = 1

    def _op_3e(self):
        # LD A, d8
        self.a = self.mmu.read_byte(self.pc)
        self.pc += 1
        self.m = 2

    def _op_3f(self):
        # CCF
        pass

    def _op_40(self):
        # LD B, B
        self.m = 1

    def _op_41(self):
        # LD B, C
        self.b = self.c
        self.m = 1

    def _op_42(self):
        # LD B, D
        self.b = self.d
        self.m = 1

    def _op_43(self):
        # LD B, E
        self.b = self.e
        self.m = 1

    def _op_44(self):
        # LD B, H
        self.b = self.h
        self.m = 1

    def _op_45(self):
        # LD B, L
        self.b = self.l
        self.m = 1

    def _op_46(self):
        # LD B, (HL)
        pass

    def _op_47(self):
        # LD B, A
        self.b = self.a
        self.m = 1

    def _op_48(self):
        # LD C, B
        self.c = self.b
        self.m = 1

    def _op_49(self):
        # LD C, C
        self.m = 1

    def _op_4a(self):
        # LD C, D
        self.c = self.d
        self.m = 1

    def _op_4b(self):
        # LD C, E
        self.c = self.e
        self.m = 1

    def _op_4c(self):
        # LD C, H
        self.c = self.h
        self.m = 1

    def _op_4d(self):
        # LD C, L
        self.c = self.l
        self.m = 1

    def _op_4e(self):
        # LD C, (HL)
        pass

    def _op_4f(self):
        # LD C, A
        self.c = self.a
        self.m = 1

    def _op_50(self):
        # LD D, B
        self.d = self.b
        self.m = 1

    def _op_51(self):
        # LD D, C
        self.d = self.c
        self.m = 1

    def _op_52(self):
        # LD D, D
        self.m = 1

    def _op_53(self):
        # LD D, E
        self.d = self.e
        self.m = 1

    def _op_54(self):
        # LD D, H
        self.d = self.h
        self.m = 1

    def _op_55(self):
        # LD D, L
        self.d = self.l
        self.m = 1

    def _op_56(self):
        # LD D, (HL)
        self.d = self.mmu.read_byte(self.h << 8 + self.l)

    def _op_57(self):
        # LD D, A
        self.d = self.a
        self.m = 1

    def _op_58(self):
        # LD E, B
        self.e = self.b
        self.m = 1

    def _op_59(self):
        # LD E, C
        self.e = self.c
        self.m = 1

    def _op_5a(self):
        # LD E, D
        self.e = self.d
        self.m = 1

    def _op_5b(self):
        # LD E, E
        self.m = 1

    def _op_5c(self):
        # LD E, H
        self.e = self.h
        self.m = 1

    def _op_5d(self):
        # LD E, L
        self.e = self.l
        self.m = 1

    def _op_5e(self):
        # LD E, (HL)
        self.e = self.mmu.read_byte(self.h << 8 + self.l)

    def _op_5f(self):
        # LD E, A
        self.e = self.a
        self.m = 1

    def _op_60(self):
        # LD H, B
        self.h = self.b
        self.m = 1

    def _op_61(self):
        # LD H, C
        self.h = self.c
        self.m = 1

    def _op_62(self):
        # LD H, D
        self.h = self.d
        self.m = 1

    def _op_63(self):
        # LD H, E
        self.h = self.e
        self.m = 1

    def _op_64(self):
        # LD H, H
        self.m = 1

    def _op_65(self):
        # LD H, L
        self.h = self.l
        self.m = 1

    def _op_66(self):
        # LD H, (HL)
        self.h = self.mmu.read_byte(self.h << 8 + self.l)

    def _op_67(self):
        # LD H, A
        self.h = self.a
        self.m = 1

    def _op_68(self):
        # LD L, B
        self.l = self.b
        self.m = 1

    def _op_69(self):
        # LD L, C
        self.l = self.c
        self.m = 1

    def _op_6a(self):
        # LD L, D
        self.l = self.d
        self.m = 1

    def _op_6b(self):
        # LD L, E
        self.l = self.e
        self.m = 1

    def _op_6c(self):
        # LD L, H
        self.l = self.h
        self.m = 1

    def _op_6d(self):
        # LD L, L
        self.m = 1

    def _op_6e(self):
        # LD L, (HL)
        pass

    def _op_6f(self):
        # LD L, A
        self.l = self.a
        self.m = 1

    def _op_70(self):
        # LD (HL), B
        pass

    def _op_71(self):
        # LD (HL), C
        pass

    def _op_72(self):
        # LD (HL), D
        pass

    def _op_73(self):
        # LD (HL), E
        pass

    def _op_74(self):
        # LD (HL), H
        pass

    def _op_75(self):
        # LD (HL), L
        pass

    def _op_76(self):
        # HALT
        pass

    def _op_77(self):
        # LD (HL), A
        pass

    def _op_78(self):
        # LD A, B
        self.a = self.b
        self.m = 1

    def _op_79(self):
        # LD A, C
        self.a = self.c
        self.m = 1

    def _op_7a(self):
        # LD A, D
        self.a = self.d
        self.m = 1

    def _op_7b(self):
        # LD A, E
        self.a = self.e
        self.m = 1

    def _op_7c(self):
        # LD A, H
        self.a = self.h
        self.m = 1

    def _op_7d(self):
        # LD A, L
        self.a = self.l
        self.m = 1

    def _op_7e(self):
        # LD A, (HL)
        pass

    def _op_7f(self):
        # LD A, A
        self.m = 1

    def _op_80(self):
        # ADD A, B
        if (self.a & 0xf) + (self.b & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.b > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.b) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_81(self):
        # ADD A, C
        if (self.a & 0xf) + (self.c & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.c > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.c) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_82(self):
        # ADD A, D
        if (self.a & 0xf) + (self.d & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.d > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.d) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_83(self):
        # ADD A, E
        if (self.a & 0xf) + (self.e & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.e > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.e) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_84(self):
        # ADD A, H
        if (self.a & 0xf) + (self.h & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.h > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.h) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_85(self):
        # ADD A, L
        if (self.a & 0xf) + (self.l & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.l > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.l) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_86(self):
        # ADD A, (HL)
        pass

    def _op_87(self):
        # ADD A, A
        if (self.a & 0xf) + (self.a & 0xf) > 0xf:
            self.hc_flag |= 1
        if self.a + self.a > 0xff:
            self.carry_flag |= 1
        self.a = (self.a + self.a) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_88(self):
        # ADC A, B
        pass

    def _op_89(self):
        # ADC A, C
        pass

    def _op_8a(self):
        # ADC A, D
        pass

    def _op_8b(self):
        # ADC A, E
        pass

    def _op_8c(self):
        # ADC A, H
        pass

    def _op_8d(self):
        # ADC A, L
        pass

    def _op_8e(self):
        # ADC A, (HL)
        pass

    def _op_8f(self):
        # ADC A, A
        pass

    def _op_90(self):
        # SUB A, B
        self.sub_flag = 1
        if (self.a & 0xf) < (self.b & 0xf):
            self.hc_flag |= 1
        if self.a < self.b > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.b) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_91(self):
        # SUB A, C
        self.sub_flag = 1
        if (self.a & 0xf) < (self.c & 0xf):
            self.hc_flag |= 1
        if self.a < self.c > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.c) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_92(self):
        # SUB A, D
        self.sub_flag = 1
        if (self.a & 0xf) < (self.d & 0xf):
            self.hc_flag |= 1
        if self.a < self.d > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.d) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_93(self):
        # SUB A, E
        self.sub_flag = 1
        if (self.a & 0xf) < (self.e & 0xf):
            self.hc_flag |= 1
        if self.a < self.e > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.e) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_94(self):
        # SUB A, H
        self.sub_flag = 1
        if (self.a & 0xf) < (self.h & 0xf):
            self.hc_flag |= 1
        if self.a < self.h > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.h) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_95(self):
        # SUB A, L
        self.sub_flag = 1
        if (self.a & 0xf) < (self.l & 0xf):
            self.hc_flag |= 1
        if self.a < self.l > 0xff:
            self.carry_flag |= 1
        self.a = (self.a - self.l) & 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_96(self):
        # SUB A, (HL)
        pass

    def _op_97(self):
        # SUB A, A
        self.sub_flag = 1
        self.a = 0
        self.zero_flag |= 1
        self.m = 1

    def _op_98(self):
        # SBC A, B
        pass

    def _op_99(self):
        # SBC A, C
        pass

    def _op_9a(self):
        # SBC A, D
        pass

    def _op_9b(self):
        # SBC A, E
        pass

    def _op_9c(self):
        # SBC A, H
        pass

    def _op_9d(self):
        # SBC A, L
        pass

    def _op_9e(self):
        # SBC A, (HL)
        pass

    def _op_9f(self):
        # SBC A, A
        pass

    def _op_a0(self):
        # AND B
        # possible half carry flag set on every AND op
        self.a &= self.b
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a1(self):
        # AND C
        self.a &= self.c
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a2(self):
        # AND D
        self.a &= self.d
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a3(self):
        # AND E
        self.a &= self.e
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a4(self):
        # AND H
        self.a &= self.h
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a5(self):
        # AND L
        self.a &= self.l
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a6(self):
        # AND (HL)
        self.a &= self.mmu.read_byte((self.h << 8) + self.l)
        self.a &= 255
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 2

    def _op_a7(self):
        # AND A
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a8(self):
        # XOR B
        self.a ^= self.b
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_a9(self):
        # XOR C
        self.a ^= self.c
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_aa(self):
        # XOR D
        self.a ^= self.d
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_ab(self):
        # XOR E
        self.a ^= self.e
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_ac(self):
        # XOR H
        self.a ^= self.h
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_ad(self):
        # XOR L
        self.a ^= self.l
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_ae(self):
        # XOR (HL)
        self.a ^= self.mmu.read_byte((self.h << 8) + self.l)
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 2

    def _op_af(self):
        # XOR A
        self.a = 0
        self.zero_flag |= 1
        self.m = 1

    def _op_b0(self):
        # OR B
        self.a |= self.b
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b1(self):
        # OR C
        self.a |= self.c
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b2(self):
        # OR D
        self.a |= self.d
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b3(self):
        # OR E
        self.a |= self.e
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b4(self):
        # OR H
        self.a |= self.h
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b5(self):
        # OR L
        self.a |= self.l
        self.a &= 0xff
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b6(self):
        # OR (HL)
        pass

    def _op_b7(self):
        # OR A
        if self.a == 0:
            self.zero_flag |= 1
        self.m = 1

    def _op_b8(self):
        # CP B
        if self.a == self.b:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.b & 0xf):
            self.hc_flag |= 1
        if self.a < self.b:
            self.carry_flag |= 1
        self.m = 1

    def _op_b9(self):
        # CP C
        if self.a == self.c:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.c & 0xf):
            self.hc_flag |= 1
        if self.a < self.c:
            self.carry_flag |= 1
        self.m = 1

    def _op_ba(self):
        # CP D
        if self.a == self.d:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.d & 0xf):
            self.hc_flag |= 1
        if self.a < self.d:
            self.carry_flag |= 1
        self.m = 1

    def _op_bb(self):
        # CP E
        if self.a == self.e:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.e & 0xf):
            self.hc_flag |= 1
        if self.a < self.e:
            self.carry_flag |= 1
        self.m = 1

    def _op_bc(self):
        # CP H
        if self.a == self.h:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.h & 0xf):
            self.hc_flag |= 1
        if self.a < self.h:
            self.carry_flag |= 1
        self.m = 1

    def _op_bd(self):
        # CP L
        if self.a == self.l:
            self.zero_flag |= 1
        if (self.a & 0xf) < (self.l & 0xf):
            self.hc_flag |= 1
        if self.a < self.l:
            self.carry_flag |= 1
        self.m = 1

    def _op_be(self):
        # CP (HL)
        pass

    def _op_bf(self):
        # CP A
        self.zero_flag |= 1
        self.m = 1

    def _op_c0(self):
        # RET NZ
        pass

    def _op_c1(self):
        # POP BC
        pass

    def _op_c2(self):
        # JP NZ, a16
        pass

    def _op_c3(self):
        # JP a16
        pass

    def _op_c4(self):
        # CALL NZ, a16
        pass

    def _op_c5(self):
        # PUSH BC
        pass

    def _op_c6(self):
        # ADD A, d8
        pass

    def _op_c7(self):
        # RST 00H
        pass

    def _op_c8(self):
        # RET Z
        pass

    def _op_c9(self):
        # RET
        pass

    def _op_ca(self):
        # JP Z, a16
        pass

    def _op_cb(self):
        # map to CB table
        pass

    def _op_cc(self):
        # CALL Z, a16
        pass

    def _op_cd(self):
        # CALL a16
        pass

    def _op_ce(self):
        # ADC A, d8
        pass

    def _op_cf(self):
        # RST 08H
        pass

    def _op_d0(self):
        # RET NC
        pass

    def _op_d1(self):
        # POP DE
        pass

    def _op_d2(self):
        # JP NC, a16
        pass

    def _op_d3(self):
        # NOT IMP
        pass

    def _op_d4(self):
        # CALL NC, a16
        pass

    def _op_d5(self):
        # PUSH DE
        pass

    def _op_d6(self):
        # SUB d8
        pass

    def _op_d7(self):
        # RST 10H
        pass

    def _op_d8(self):
        # RET C
        pass

    def _op_d9(self):
        # RETI
        pass

    def _op_da(self):
        # JP C, a16
        pass

    def _op_db(self):
        # NOT IMP
        pass

    def _op_dc(self):
        # CALL C, a16
        pass

    def _op_dd(self):
        # NOT IMP
        pass

    def _op_de(self):
        # SBC A, d8
        pass

    def _op_df(self):
        # RST 18H
        pass

    def _op_e0(self):
        # LDH (a8), A
        pass

    def _op_e1(self):
        # POP HL
        pass

    def _op_e2(self):
        # LD (C), A
        pass

    def _op_e3(self):
        # NOT IMP
        pass

    def _op_e4(self):
        # NOT IMP
        pass

    def _op_e5(self):
        # PUSH HL
        pass

    def _op_e6(self):
        # AND d8
        pass

    def _op_e7(self):
        # RST 20H
        pass

    def _op_e8(self):
        # ADD SP, r8
        pass

    def _op_e9(self):
        # JP (HL)
        pass

    def _op_ea(self):
        # LD (a16), A
        pass

    def _op_eb(self):
        # NOT IMP
        pass

    def _op_ec(self):
        # NOT IMP
        pass

    def _op_ed(self):
        # NOT IMP
        pass

    def _op_ee(self):
        # XOR d8
        pass

    def _op_ef(self):
        # RST 28H
        pass

    def _op_f0(self):
        # LDH A, (a8)
        pass

    def _op_f1(self):
        # POP AF
        pass

    def _op_f2(self):
        # LD A, (C)
        pass

    def _op_f3(self):
        # DI
        pass

    def _op_f4(self):
        # NOT IMP
        pass

    def _op_f5(self):
        # PUSH AF
        pass

    def _op_f6(self):
        # OR d8
        pass

    def _op_f7(self):
        # RST 30H
        pass

    def _op_f8(self):
        # LD HL, SP+r8
        pass

    def _op_f9(self):
        # LD SP, HL
        pass

    def _op_fa(self):
        # LD A, (a16)
        pass

    def _op_fb(self):
        # EI
        pass

    def _op_fc(self):
        # NOT IMP
        pass

    def _op_fd(self):
        # NOT IMP
        pass

    def _op_fe(self):
        # CP d8
        pass

    def _op_ff(self):
        # RST 38H
        pass
