"""
GameBoy cpu module
"""
__author__ = 'cjpowell'
from mmu import MMU


class Cpu(object):
    """
    Cpu class that emulates the GameBoy cpu for the emulator.
    """

    def __init__(self):
        self.pc = 0
        self.sp = 0
        self.mmu = MMU()
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0
        self.m = 0
        self.t = 0
        self.zero_flag = 0
        self.sub_flag = 0
        self.hc_flag = 0
        self.carry_flag = 0
        self.clock = {'m': 0, 't': 0}
        self.opcodes = [self._op_00, self._op_01, self._op_02, self._op_03,
                        self._op_04, self._op_05, self._op_06, self._op_07,
                        self._op_08, self._op_09, self._op_0a, self._op_0b,
                        self._op_0c, self._op_0d, self._op_0e, self._op_0f,
                        self._op_10, self._op_11, self._op_12, self._op_13,
                        self._op_14, self._op_15, self._op_16, self._op_17,
                        self._op_18, self._op_19, self._op_1a, self._op_1b,
                        self._op_1c, self._op_1d, self._op_1e, self._op_1f,
                        self._op_20, self._op_21, self._op_22, self._op_23,
                        self._op_24, self._op_25, self._op_26, self._op_27,
                        self._op_28, self._op_29, self._op_2a, self._op_2b,
                        self._op_2c, self._op_2d, self._op_2e, self._op_2f,
                        self._op_30, self._op_31, self._op_32, self._op_33,
                        self._op_34, self._op_35, self._op_36, self._op_37,
                        self._op_38, self._op_39, self._op_3a, self._op_3b,
                        self._op_3c, self._op_3d, self._op_3e, self._op_3f,
                        self._op_40, self._op_41, self._op_42, self._op_43,
                        self._op_44, self._op_45, self._op_46, self._op_47,
                        self._op_48, self._op_49, self._op_4a, self._op_4b,
                        self._op_4c, self._op_4d, self._op_4e, self._op_4f,
                        self._op_50, self._op_51, self._op_52, self._op_53,
                        self._op_54, self._op_55, self._op_56, self._op_57,
                        self._op_58, self._op_59, self._op_5a, self._op_5b,
                        self._op_5c, self._op_5d, self._op_5e, self._op_5f,
                        self._op_60, self._op_61, self._op_62, self._op_63,
                        self._op_64, self._op_65, self._op_66, self._op_67,
                        self._op_68, self._op_69, self._op_6a, self._op_6b,
                        self._op_6c, self._op_6d, self._op_6e, self._op_6f,
                        self._op_70, self._op_71, self._op_72, self._op_73,
                        self._op_74, self._op_75, self._op_76, self._op_77,
                        self._op_78, self._op_79, self._op_7a, self._op_7b,
                        self._op_7c, self._op_7d, self._op_7e, self._op_7f,
                        self._op_80, self._op_81, self._op_82, self._op_83,
                        self._op_84, self._op_85, self._op_86, self._op_87,
                        self._op_88, self._op_89, self._op_8a, self._op_8b,
                        self._op_8c, self._op_8d, self._op_8e, self._op_8f,
                        self._op_90, self._op_91, self._op_92, self._op_93,
                        self._op_94, self._op_95, self._op_96, self._op_97,
                        self._op_98, self._op_99, self._op_9a, self._op_9b,
                        self._op_9c, self._op_9d, self._op_9e, self._op_9f,
                        self._op_a0, self._op_a1, self._op_a2, self._op_a3,
                        self._op_a4, self._op_a5, self._op_a6, self._op_a7,
                        self._op_a8, self._op_a9, self._op_aa, self._op_ab,
                        self._op_ac, self._op_ad, self._op_ae, self._op_af,
                        self._op_b0, self._op_b1, self._op_b2, self._op_b3,
                        self._op_b4, self._op_b5, self._op_b6, self._op_b7,
                        self._op_b8, self._op_b9, self._op_ba, self._op_bb,
                        self._op_bc, self._op_bd, self._op_be, self._op_bf,
                        self._op_c0, self._op_c1, self._op_c2, self._op_c3,
                        self._op_c4, self._op_c5, self._op_c6, self._op_c7,
                        self._op_c8, self._op_c9, self._op_ca, self._op_cb,
                        self._op_cc, self._op_cd, self._op_ce, self._op_cf,
                        self._op_d0, self._op_d1, self._op_d2, self._op_d3,
                        self._op_d4, self._op_d5, self._op_d6, self._op_d7,
                        self._op_d8, self._op_d9, self._op_da, self._op_db,
                        self._op_dc, self._op_dd, self._op_de, self._op_df,
                        self._op_e0, self._op_e1, self._op_e2, self._op_e3,
                        self._op_e4, self._op_e5, self._op_e6, self._op_e7,
                        self._op_e8, self._op_e9, self._op_ea, self._op_eb,
                        self._op_ec, self._op_ed, self._op_ee, self._op_ef,
                        self._op_f0, self._op_f1, self._op_f2, self._op_f3,
                        self._op_f4, self._op_f5, self._op_f6, self._op_f7,
                        self._op_f8, self._op_f9, self._op_fa, self._op_fb,
                        self._op_fc, self._op_fd, self._op_fe, self._op_ff]

    def _op_00(self):
        # NOP
        self.m = 1

    def _op_01(self):
        # LD BC, d16
        self.c = self.mmu.read_byte(self.pc)
        self.b = self.mmu.read_byte(self.pc + 1)
        self.pc += 2
        self.m = 3

    def _op_02(self):
        # LD (BC), A
        pass

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
        # LD (a16), SP
        pass

    def _op_09(self):
        # ADD HL, BC
        pass

    def _op_0a(self):
        # LD A, (BC)
        self.a = self.mmu.read_byte((self.b << 8) | self.c)
        self.m = 2

    def _op_0b(self):
        # DEC BC
        pass

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
        pass

    def _op_0f(self):
        # RRCA
        pass

    def _op_10(self):
        # STOP 0
        pass

    def _op_11(self):
        # LD DE, d16
        pass

    def _op_12(self):
        # LD (DE), A
        pass

    def _op_13(self):
        # INC DE
        pass

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
        pass

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
        pass

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
        pass

    def _op_1f(self):
        # RRA
        pass

    def _op_20(self):
        # JR NZ, r8
        pass

    def _op_21(self):
        # LD HL, d16
        pass

    def _op_22(self):
        # LD (HL+), A
        pass

    def _op_23(self):
        # INC HL
        pass

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
        pass

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
        pass

    def _op_2e(self):
        # LD L, d8
        pass

    def _op_2f(self):
        # CPL
        pass

    def _op_30(self):
        # JR NC, r8
        pass

    def _op_31(self):
        # LD SP, d16
        pass

    def _op_32(self):
        # LD (HL-), A
        pass

    def _op_33(self):
        # INC SP
        pass

    def _op_34(self):
        # INC (HL)
        pass

    def _op_35(self):
        # DEC (HL)
        pass

    def _op_36(self):
        # LD (HL), d8
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
        pass

    def _op_3c(self):
        # INC A
        pass

    def _op_3d(self):
        # DEC A
        pass

    def _op_3e(self):
        # LD A, d8
        pass

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
        pass

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
        pass

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
        pass

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
        pass

    def _op_81(self):
        # ADD A, C
        pass

    def _op_82(self):
        # ADD A, D
        pass

    def _op_83(self):
        # ADD A, E
        pass

    def _op_84(self):
        # ADD A, H
        pass

    def _op_85(self):
        # ADD A, L
        pass

    def _op_86(self):
        # ADD A, (HL)
        pass

    def _op_87(self):
        # ADD A, A
        pass

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

    def _subr_b(self):
        pass

    def _subr_c(self):
        pass

    def _subr_d(self):
        pass

    def _subr_e(self):
        pass

    def _subr_h(self):
        pass

    def _subr_l(self):
        pass

    def _subhl(self):
        pass

    def _subr_a(self):
        pass

    def _sbcr_b(self):
        pass

    def _sbcr_c(self):
        pass

    def _sbcr_d(self):
        pass

    def _sbcr_e(self):
        pass

    def _sbcr_h(self):
        pass

    def _sbcr_l(self):
        pass

    def _sbchl(self):
        pass

    def _sbcr_a(self):
        pass

    def _andr_b(self):
        pass

    def _andr_c(self):
        pass

    def _andr_d(self):
        pass

    def _andr_e(self):
        pass

    def _andr_h(self):
        pass

    def _andr_l(self):
        pass

    def _andhl(self):
        pass

    def _andr_a(self):
        pass

    def _xorr_b(self):
        pass

    def _xorr_c(self):
        pass

    def _xorr_d(self):
        pass

    def _xorr_e(self):
        pass

    def _xorr_h(self):
        pass

    def _xorr_l(self):
        pass

    def _xorhl(self):
        pass

    def _xorr_a(self):
        pass

    def _orr_b(self):
        pass

    def _orr_c(self):
        pass

    def _orr_d(self):
        pass

    def _orr_e(self):
        pass

    def _orr_h(self):
        pass

    def _orr_l(self):
        pass

    def _orhl(self):
        pass

    def _orr_a(self):
        pass

    def _cpr_b(self):
        pass

    def _cpr_c(self):
        pass

    def _cpr_d(self):
        pass

    def _cpr_e(self):
        pass

    def _cpr_h(self):
        pass

    def _cpr_l(self):
        pass

    def _cphl(self):
        pass

    def _cpr_a(self):
        pass

    def _retnz(self):
        pass

    def _popbc(self):
        pass

    def _jpnznn(self):
        pass

    def _jpnn(self):
        pass

    def _callnznn(self):
        pass

    def _pushbc(self):
        pass

    def _addn(self):
        pass

    def _rst00(self):
        pass

    def _retz(self):
        pass

    def _ret(self):
        pass

    def _jpznn(self):
        pass

    def _mapcb(self):
        pass

    def _callznn(self):
        pass

    def _callnn(self):
        pass

    def _adcn(self):
        pass

    def _rst08(self):
        pass

    def _retnc(self):
        pass

    def _popde(self):
        pass

    def _jpncnn(self):
        pass

    def _xx(self):
        pass

    def _callncnn(self):
        pass

    def _pushde(self):
        pass

    def _subn(self):
        pass

    def _rst10(self):
        pass

    def _retc(self):
        pass

    def _reti(self):
        pass

    def _jpcnn(self):
        pass

    def _callcnn(self):
        pass

    def _sbcn(self):
        pass

    def _rst18(self):
        pass

    def _ldiona(self):
        pass

    def _pophl(self):
        pass

    def _ldioca(self):
        pass

    def _pushhl(self):
        pass

    def _andn(self):
        pass

    def _rst20(self):
        pass

    def _addspn(self):
        pass

    def _jphl(self):
        pass

    def _ldmma(self):
        pass

    def _xorn(self):
        pass

    def _rst28(self):
        pass

    def _ldaion(self):
        pass

    def _popaf(self):
        pass

    def _ldaioc(self):
        pass

    def _di(self):
        pass

    def _pushaf(self):
        pass

    def _orn(self):
        pass

    def _rst30(self):
        pass

    def _ldhlspn(self):
        pass

    def _ldamm(self):
        pass

    def _ei(self):
        pass

    def _cpn(self):
        pass

    def _rst38(self):
        pass