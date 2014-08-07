"""
GameBoy CPU module
"""
__author__ = 'cjpowell'


class CPU(object):
    """
    CPU class that emulates the GameBoy cpu for the emulator.
    """
    def __init__(self):
        self.pc = 0
        self.sp = 0
        self.registers = {'a': 0,
                          'b': 0,
                          'c': 0,
                          'd': 0,
                          'e': 0,
                          'f': 0,
                          'h': 0,
                          'l': 0,
                          'm': 0,
                          't': 0}
        self.clock = {'m': 0, 't': 0}
        self.op_map = [self._nop, self._ldbcnn, self._LDBCmA, self._INCBC,
                       self._INCr_b, self._DECr_b, self._LDrn_b, self._RLCA,
                       self._LDmmSP, self._ADDHLBC, self._LDABCm, self._DECBC,
                       self._INCr_c, self._DECr_c, self._LDrn_c, self._RRCA,
                       self._DJNZn, self._LDDEnn, self._LDDEmA, self._INCDE,
                       self._INCr_d, self._DECr_d, self._LDrn_d, self._RLA,
                       self._JRn, self._ADDHLDE, self._LDADEm, self._DECDE,
                       self._INCr_e, self._DECr_e, self._LDrn_e, self._RRA,
                       self._JRNZn, self._LDHLnn, self._LDHLIA, self._INCHL,
                       self._INCr_h, self._DECr_h, self._LDrn_h, self._DAA,
                       self._JRZn, self._ADDHLHL, self._LDAHLI, self._DECHL,
                       self._INCr_l, self._DECr_l, self._LDrn_l, self._CPL,
                       self._JRNCn, self._LDSPnn, self._LDHLDA, self._INCSP,
                       self._INCHLm, self._DECHLm, self._LDHLmn, self._SCF,
                       self._JRCn, self._ADDHLSP, self._LDAHLD, self._DECSP,
                       self._INCr_a, self._DECr_a, self._LDrn_a, self._CCF,
                       self._LDrr_bb, self._LDrr_bc, self._LDrr_bd, self._LDrr_be,
                       self._LDrr_bh, self._LDrr_bl, self._LDrHLm_b, self._LDrr_ba,
                       self._LDrr_cb, self._LDrr_cc, self._LDrr_cd, self._LDrr_ce,
                       self._LDrr_ch, self._LDrr_cl, self._LDrHLm_c, self._LDrr_ca,
                       self._LDrr_db, self._LDrr_dc, self._LDrr_dd, self._LDrr_de,
                       self._LDrr_dh, self._LDrr_dl, self._LDrHLm_d, self._LDrr_da,
                       self._LDrr_eb, self._LDrr_ec, self._LDrr_ed, self._LDrr_ee,
                       self._LDrr_eh, self._LDrr_el, self._LDrHLm_e, self._LDrr_ea,
                       self._LDrr_hb, self._LDrr_hc, self._LDrr_hd, self._LDrr_he,
                       self._LDrr_hh, self._LDrr_hl, self._LDrHLm_h, self._LDrr_ha,
                       self._LDrr_lb, self._LDrr_lc, self._LDrr_ld, self._LDrr_le,
                       self._LDrr_lh, self._LDrr_ll, self._LDrHLm_l, self._LDrr_la,
                       self._LDHLmr_b, self._LDHLmr_c, self._LDHLmr_d, self._LDHLmr_e,
                       self._LDHLmr_h, self._LDHLmr_l, self._HALT, self._LDHLmr_a,
                       self._LDrr_ab, self._LDrr_ac, self._LDrr_ad, self._LDrr_ae,
                       self._LDrr_ah, self._LDrr_al, self._LDrHLm_a, self._LDrr_aa,
                       self._ADDr_b, self._ADDr_c, self._ADDr_d, self._ADDr_e,
                       self._ADDr_h, self._ADDr_l, self._ADDHL, self._ADDr_a,
                       self._ADCr_b, self._ADCr_c, self._ADCr_d, self._ADCr_e,
                       self._ADCr_h, self._ADCr_l, self._ADCHL, self._ADCr_a,
                       self._SUBr_b, self._SUBr_c, self._SUBr_d, self._SUBr_e,
                       self._SUBr_h, self._SUBr_l, self._SUBHL, self._SUBr_a,
                       self._SBCr_b, self._SBCr_c, self._SBCr_d, self._SBCr_e,
                       self._SBCr_h, self._SBCr_l, self._SBCHL, self._SBCr_a,
                       self._ANDr_b, self._ANDr_c, self._ANDr_d, self._ANDr_e,
                       self._ANDr_h, self._ANDr_l, self._ANDHL, self._ANDr_a,
                       self._XORr_b, self._XORr_c, self._XORr_d, self._XORr_e,
                       self._XORr_h, self._XORr_l, self._XORHL, self._XORr_a,
                       self._ORr_b, self._ORr_c, self._ORr_d, self._ORr_e,
                       self._ORr_h, self._ORr_l, self._ORHL, self._ORr_a,
                       self._CPr_b, self._CPr_c, self._CPr_d, self._CPr_e,
                       self._CPr_h, self._CPr_l, self._CPHL, self._CPr_a,
                       self._RETNZ, self._POPBC, self._JPNZnn, self._JPnn,
                       self._CALLNZnn, self._PUSHBC, self._ADDn, self._RST00,
                       self._RETZ, self._RET, self._JPZnn, self._MAPcb,
                       self._CALLZnn, self._CALLnn, self._ADCn, self._RST08,
                       self._RETNC, self._POPDE, self._JPNCnn, self._XX,
                       self._CALLNCnn, self._PUSHDE, self._SUBn, self._RST10,
                       self._RETC, self._RETI, self._JPCnn, self._XX,
                       self._CALLCnn, self._XX, self._SBCn, self._RST18,
                       self._LDIOnA, self._POPHL, self._LDIOCA, self._XX,
                       self._XX, self._PUSHHL, self._ANDn, self._RST20,
                       self._ADDSPn, self._JPHL, self._LDmmA, self._XX,
                       self._XX, self._XX, self._XORn, self._RST28,
                       self._LDAIOn, self._POPAF, self._LDAIOC, self._DI,
                       self._XX, self._PUSHAF, self._ORn, self._RST30,
                       self._LDHLSPn, self._XX, self._LDAmm, self._EI,
                       self._XX, self._XX, self._CPn, self._RST38]
        
    def _nop(self):
        self.registers['m'] = 1
        
    def _ldbcnn(self):
        self.registers['m'] = 3

    def _LDBCmA(self):
        pass

    def _INCBC(self):
        pass

    def _INCr_b(self):
        pass

    def _DECr_b(self):
        pass

    def _LDrn_b(self):
        pass

    def _RLCA(self):
        pass

    def _LDmmSP(self):
        pass

    def _ADDHLBC(self):
        pass

    def _LDABCm(self):
        pass

    def _DECBC(self):
        pass

    def _INCr_c(self):
        pass

    def _DECr_c(self):
        pass

    def _LDrn_c(self):
        pass

    def _RRCA(self):
        pass

    def _DJNZn(self):
        pass

    def _LDDEnn(self):
        pass

    def _LDDEmA(self):
        pass

    def _INCDE(self):
        pass

    def _INCr_d(self):
        pass

    def _DECr_d(self):
        pass

    def _LDrn_d(self):
        pass

    def _RLA(self):
        pass

    def _JRn(self):
        pass

    def _ADDHLDE(self):
        pass

    def _LDADEm(self):
        pass

    def _DECDE(self):
        pass

    def _INCr_e(self):
        pass

    def _DECr_e(self):
        pass

    def _LDrn_e(self):
        pass

    def _RRA(self):
        pass

    def _JRNZn(self):
        pass

    def _LDHLnn(self):
        pass

    def _LDHLIA(self):
        pass

    def _INCHL(self):
        pass

    def _INCr_h(self):
        pass

    def _DECr_h(self):
        pass

    def _LDrn_h(self):
        pass

    def _DAA(self):
        pass

    def _JRZn(self):
        pass

    def _ADDHLHL(self):
        pass

    def _LDAHLI(self):
        pass

    def _DECHL(self):
        pass

    def _INCr_l(self):
        pass

    def _DECr_l(self):
        pass

    def _LDrn_l(self):
        pass

    def _CPL(self):
        pass

    def _JRNCn(self):
        pass

    def _LDSPnn(self):
        pass

    def _LDHLDA(self):
        pass

    def _INCSP(self):
        pass

    def _INCHLm(self):
        pass

    def _DECHLm(self):
        pass

    def _LDHLmn(self):
        pass

    def _SCF(self):
        pass

    def _JRCn(self):
        pass

    def _ADDHLSP(self):
        pass

    def _LDAHLD(self):
        pass

    def _DECSP(self):
        pass

    def _INCr_a(self):
        pass

    def _DECr_a(self):
        pass

    def _LDrn_a(self):
        pass

    def _CCF(self):
        pass

    def _LDrr_bb(self):
        pass

    def _LDrr_bc(self):
        pass

    def _LDrr_bd(self):
        pass

    def _LDrr_be(self):
        pass

                       self._LDrr_bh, self._LDrr_bl, self._LDrHLm_b, self._LDrr_ba,
                       self._LDrr_cb, self._LDrr_cc, self._LDrr_cd, self._LDrr_ce,
                       self._LDrr_ch, self._LDrr_cl, self._LDrHLm_c, self._LDrr_ca,
                       self._LDrr_db, self._LDrr_dc, self._LDrr_dd, self._LDrr_de,
                       self._LDrr_dh, self._LDrr_dl, self._LDrHLm_d, self._LDrr_da,
                       self._LDrr_eb, self._LDrr_ec, self._LDrr_ed, self._LDrr_ee,
                       self._LDrr_eh, self._LDrr_el, self._LDrHLm_e, self._LDrr_ea,
                       self._LDrr_hb, self._LDrr_hc, self._LDrr_hd, self._LDrr_he,
                       self._LDrr_hh, self._LDrr_hl, self._LDrHLm_h, self._LDrr_ha,
                       self._LDrr_lb, self._LDrr_lc, self._LDrr_ld, self._LDrr_le,
                       self._LDrr_lh, self._LDrr_ll, self._LDrHLm_l, self._LDrr_la,
                       self._LDHLmr_b, self._LDHLmr_c, self._LDHLmr_d, self._LDHLmr_e,
                       self._LDHLmr_h, self._LDHLmr_l, self._HALT, self._LDHLmr_a,
                       self._LDrr_ab, self._LDrr_ac, self._LDrr_ad, self._LDrr_ae,
                       self._LDrr_ah, self._LDrr_al, self._LDrHLm_a, self._LDrr_aa,
                       self._ADDr_b, self._ADDr_c, self._ADDr_d, self._ADDr_e,
                       self._ADDr_h, self._ADDr_l, self._ADDHL, self._ADDr_a,
                       self._ADCr_b, self._ADCr_c, self._ADCr_d, self._ADCr_e,
                       self._ADCr_h, self._ADCr_l, self._ADCHL, self._ADCr_a,
                       self._SUBr_b, self._SUBr_c, self._SUBr_d, self._SUBr_e,
                       self._SUBr_h, self._SUBr_l, self._SUBHL, self._SUBr_a,
                       self._SBCr_b, self._SBCr_c, self._SBCr_d, self._SBCr_e,
                       self._SBCr_h, self._SBCr_l, self._SBCHL, self._SBCr_a,
                       self._ANDr_b, self._ANDr_c, self._ANDr_d, self._ANDr_e,
                       self._ANDr_h, self._ANDr_l, self._ANDHL, self._ANDr_a,
                       self._XORr_b, self._XORr_c, self._XORr_d, self._XORr_e,
                       self._XORr_h, self._XORr_l, self._XORHL, self._XORr_a,
                       self._ORr_b, self._ORr_c, self._ORr_d, self._ORr_e,
                       self._ORr_h, self._ORr_l, self._ORHL, self._ORr_a,
                       self._CPr_b, self._CPr_c, self._CPr_d, self._CPr_e,
                       self._CPr_h, self._CPr_l, self._CPHL, self._CPr_a,
                       self._RETNZ, self._POPBC, self._JPNZnn, self._JPnn,
                       self._CALLNZnn, self._PUSHBC, self._ADDn, self._RST00,
                       self._RETZ, self._RET, self._JPZnn, self._MAPcb,
                       self._CALLZnn, self._CALLnn, self._ADCn, self._RST08,
                       self._RETNC, self._POPDE, self._JPNCnn, self._XX,
                       self._CALLNCnn, self._PUSHDE, self._SUBn, self._RST10,
                       self._RETC, self._RETI, self._JPCnn, self._XX,
                       self._CALLCnn, self._XX, self._SBCn, self._RST18,
                       self._LDIOnA, self._POPHL, self._LDIOCA, self._XX,
                       self._XX, self._PUSHHL, self._ANDn, self._RST20,
                       self._ADDSPn, self._JPHL, self._LDmmA, self._XX,
                       self._XX, self._XX, self._XORn, self._RST28,
                       self._LDAIOn, self._POPAF, self._LDAIOC, self._DI,
                       self._XX, self._PUSHAF, self._ORn, self._RST30,
                       self._LDHLSPn, self._XX, self._LDAmm, self._EI,
                       self._XX, self._XX, self._CPn, self._RST38