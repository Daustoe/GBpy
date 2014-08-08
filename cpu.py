"""
GameBoy cpu module
"""
__author__ = 'cjpowell'


class Cpu(object):
    """
    Cpu class that emulates the GameBoy cpu for the emulator.
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
        self.op_map = [self._nop, self._ldbcnn, self._ldbcma, self._incbc,
                       self._incr_b, self._decr_b, self._ldrn_b, self._rlca,
                       self._ldmmsp, self._addhlbc, self._ldabcm, self._decbc,
                       self._incr_c, self._decr_c, self._ldrn_c, self._rrca,
                       self._djnzn, self._lddenn, self._lddema, self._incde,
                       self._incr_d, self._decr_d, self._ldrn_d, self._rla,
                       self._jrn, self._addhlde, self._ldadem, self._decde,
                       self._incr_e, self._decr_e, self._ldrn_e, self._rra,
                       self._jrnzn, self._ldhlnn, self._ldhlia, self._inchl,
                       self._incr_h, self._decr_h, self._ldrn_h, self._daa,
                       self._jrzn, self._addhlhl, self._ldahli, self._dechl,
                       self._incr_l, self._decr_l, self._ldrn_l, self._cpl,
                       self._jrncn, self._ldspnn, self._ldhlda, self._incsp,
                       self._inchlm, self._dechlm, self._ldhlmn, self._scf,
                       self._jrcn, self._addhlsp, self._ldahld, self._decsp,
                       self._incr_a, self._decr_a, self._ldrn_a, self._ccf,
                       self._ldrr_bb, self._ldrr_bc, self._ldrr_bd, self._ldrr_be,
                       self._ldrr_bh, self._ldrr_bl, self._ldrhlm_b, self._ldrr_ba,
                       self._ldrr_cb, self._ldrr_cc, self._ldrr_cd, self._ldrr_ce,
                       self._ldrr_ch, self._ldrr_cl, self._ldrhlm_c, self._ldrr_ca,
                       self._ldrr_db, self._ldrr_dc, self._ldrr_dd, self._ldrr_de,
                       self._ldrr_dh, self._ldrr_dl, self._ldrhlm_d, self._ldrr_da,
                       self._ldrr_eb, self._ldrr_ec, self._ldrr_ed, self._ldrr_ee,
                       self._ldrr_eh, self._ldrr_el, self._ldrhlm_e, self._ldrr_ea,
                       self._ldrr_hb, self._ldrr_hc, self._ldrr_hd, self._ldrr_he,
                       self._ldrr_hh, self._ldrr_hl, self._ldrhlm_h, self._ldrr_ha,
                       self._ldrr_lb, self._ldrr_lc, self._ldrr_ld, self._ldrr_le,
                       self._ldrr_lh, self._ldrr_ll, self._ldrhlm_l, self._ldrr_la,
                       self._ldhlmr_b, self._ldhlmr_c, self._ldhlmr_d, self._ldhlmr_e,
                       self._ldhlmr_h, self._ldhlmr_l, self._halt, self._ldhlmr_a,
                       self._ldrr_ab, self._ldrr_ac, self._ldrr_ad, self._ldrr_ae,
                       self._ldrr_ah, self._ldrr_al, self._ldrhlm_a, self._ldrr_aa,
                       self._addr_b, self._addr_c, self._addr_d, self._addr_e,
                       self._addr_h, self._addr_l, self._addhl, self._addr_a,
                       self._adcr_b, self._adcr_c, self._adcr_d, self._adcr_e,
                       self._adcr_h, self._adcr_l, self._adchl, self._adcr_a,
                       self._subr_b, self._subr_c, self._subr_d, self._subr_e,
                       self._subr_h, self._subr_l, self._subhl, self._subr_a,
                       self._sbcr_b, self._sbcr_c, self._sbcr_d, self._sbcr_e,
                       self._sbcr_h, self._sbcr_l, self._sbchl, self._sbcr_a,
                       self._andr_b, self._andr_c, self._andr_d, self._andr_e,
                       self._andr_h, self._andr_l, self._andhl, self._andr_a,
                       self._xorr_b, self._xorr_c, self._xorr_d, self._xorr_e,
                       self._xorr_h, self._xorr_l, self._xorhl, self._xorr_a,
                       self._orr_b, self._orr_c, self._orr_d, self._orr_e,
                       self._orr_h, self._orr_l, self._orhl, self._orr_a,
                       self._cpr_b, self._cpr_c, self._cpr_d, self._cpr_e,
                       self._cpr_h, self._cpr_l, self._cphl, self._cpr_a,
                       self._retnz, self._popbc, self._jpnznn, self._jpnn,
                       self._callnznn, self._pushbc, self._addn, self._rst00,
                       self._retz, self._ret, self._jpznn, self._mapcb,
                       self._callznn, self._callnn, self._adcn, self._rst08,
                       self._retnc, self._popde, self._jpncnn, self._xx,
                       self._callncnn, self._pushde, self._subn, self._rst10,
                       self._retc, self._reti, self._jpcnn, self._xx,
                       self._callcnn, self._xx, self._sbcn, self._rst18,
                       self._ldiona, self._pophl, self._ldioca, self._xx,
                       self._xx, self._pushhl, self._andn, self._rst20,
                       self._addspn, self._jphl, self._ldmma, self._xx,
                       self._xx, self._xx, self._xorn, self._rst28,
                       self._ldaion, self._popaf, self._ldaioc, self._di,
                       self._xx, self._pushaf, self._orn, self._rst30,
                       self._ldhlspn, self._xx, self._ldamm, self._ei,
                       self._xx, self._xx, self._cpn, self._rst38]
        
    def _nop(self):
        self.registers['m'] = 1
        
    def _ldbcnn(self):
        self.registers['m'] = 3

    def _ldbcma(self):
        pass

    def _incbc(self):
        pass

    def _incr_b(self):
        pass

    def _decr_b(self):
        pass

    def _ldrn_b(self):
        pass

    def _rlca(self):
        pass

    def _ldmmsp(self):
        pass

    def _addhlbc(self):
        pass

    def _ldabcm(self):
        pass

    def _decbc(self):
        pass

    def _incr_c(self):
        pass

    def _decr_c(self):
        pass

    def _ldrn_c(self):
        pass

    def _rrca(self):
        pass

    def _djnzn(self):
        pass

    def _lddenn(self):
        pass

    def _lddema(self):
        pass

    def _incde(self):
        pass

    def _incr_d(self):
        pass

    def _decr_d(self):
        pass

    def _ldrn_d(self):
        pass

    def _rla(self):
        pass

    def _jrn(self):
        pass

    def _addhlde(self):
        pass

    def _ldadem(self):
        pass

    def _decde(self):
        pass

    def _incr_e(self):
        pass

    def _decr_e(self):
        pass

    def _ldrn_e(self):
        pass

    def _rra(self):
        pass

    def _jrnzn(self):
        pass

    def _ldhlnn(self):
        pass

    def _ldhlia(self):
        pass

    def _inchl(self):
        pass

    def _incr_h(self):
        pass

    def _decr_h(self):
        pass

    def _ldrn_h(self):
        pass

    def _daa(self):
        pass

    def _jrzn(self):
        pass

    def _addhlhl(self):
        pass

    def _ldahli(self):
        pass

    def _dechl(self):
        pass

    def _incr_l(self):
        pass

    def _decr_l(self):
        pass

    def _ldrn_l(self):
        pass

    def _cpl(self):
        pass

    def _jrncn(self):
        pass

    def _ldspnn(self):
        pass

    def _ldhlda(self):
        pass

    def _incsp(self):
        pass

    def _inchlm(self):
        pass

    def _dechlm(self):
        pass

    def _ldhlmn(self):
        pass

    def _scf(self):
        pass

    def _jrcn(self):
        pass

    def _addhlsp(self):
        pass

    def _ldahld(self):
        pass

    def _decsp(self):
        pass

    def _incr_a(self):
        pass

    def _decr_a(self):
        pass

    def _ldrn_a(self):
        pass

    def _ccf(self):
        pass

    def _ldrr_bb(self):
        self.registers['b'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_bc(self):
        self.registers['b'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_bd(self):
        self.registers['b'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_be(self):
        self.registers['b'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_bh(self):
        self.registers['b'] = self.registers['h']
        self.registers['m'] = 1
        
    def _ldrr_bl(self):
        self.registers['b'] = self.registers['l']
        self.registers['m'] = 1
        
    def _ldrhlm_b(self):
        pass
        
    def _ldrr_ba(self):
        self.registers['b'] = self.registers['a']
        self.registers['m'] = 1

    def _ldrr_cb(self):
        self.registers['c'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_cc(self):
        self.registers['c'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_cd(self):
        self.registers['c'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_ce(self):
        self.registers['c'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_ch(self):
        self.registers['c'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_cl(self):
        self.registers['c'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_c(self):
        pass

    def _ldrr_ca(self):
        self.registers['c'] = self.registers['a']
        self.registers['m'] = 1

    def _ldrr_db(self):
        self.registers['d'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_dc(self):
        self.registers['d'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_dd(self):
        self.registers['d'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_de(self):
        self.registers['d'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_dh(self):
        self.registers['d'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_dl(self):
        self.registers['d'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_d(self):
        pass

    def _ldrr_da(self):
        self.registers['d'] = self.registers['a']
        self.registers['m'] = 1

    def _ldrr_eb(self):
        self.registers['e'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_ec(self):
        self.registers['e'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_ed(self):
        self.registers['e'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_ee(self):
        self.registers['e'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_eh(self):
        self.registers['e'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_el(self):
        self.registers['e'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_e(self):
        pass

    def _ldrr_ea(self):
        self.registers['e'] = self.registers['a']
        self.registers['m'] = 1

    def _ldrr_hb(self):
        self.registers['h'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_hc(self):
        self.registers['h'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_hd(self):
        self.registers['h'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_he(self):
        self.registers['h'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_hh(self):
        self.registers['h'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_hl(self):
        self.registers['h'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_h(self):
        pass

    def _ldrr_ha(self):
        self.registers['h'] = self.registers['a']
        self.registers['m'] = 1

    def _ldrr_lb(self):
        self.registers['l'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_lc(self):
        self.registers['l'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_ld(self):
        self.registers['l'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_le(self):
        self.registers['l'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_lh(self):
        self.registers['l'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_ll(self):
        self.registers['l'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_l(self):
        pass

    def _ldrr_la(self):
        self.registers['l'] = self.registers['a']
        self.registers['m'] = 1

    def _ldhlmr_b(self):
        pass

    def _ldhlmr_c(self):
        pass

    def _ldhlmr_d(self):
        pass

    def _ldhlmr_e(self):
        pass

    def _ldhlmr_h(self):
        pass

    def _ldhlmr_l(self):
        pass

    def _halt(self):
        pass

    def _ldhlmr_a(self):
        pass
        
    def _ldrr_ab(self):
        self.registers['a'] = self.registers['b']
        self.registers['m'] = 1

    def _ldrr_ac(self):
        self.registers['a'] = self.registers['c']
        self.registers['m'] = 1

    def _ldrr_ad(self):
        self.registers['a'] = self.registers['d']
        self.registers['m'] = 1

    def _ldrr_ae(self):
        self.registers['a'] = self.registers['e']
        self.registers['m'] = 1

    def _ldrr_ah(self):
        self.registers['a'] = self.registers['h']
        self.registers['m'] = 1

    def _ldrr_al(self):
        self.registers['a'] = self.registers['l']
        self.registers['m'] = 1

    def _ldrhlm_a(self):
        pass

    def _ldrr_aa(self):
        self.registers['a'] = self.registers['a']
        self.registers['m'] = 1

    def _addr_b(self):
        pass

    def _addr_c(self):
        pass

    def _addr_d(self):
        pass

    def _addr_e(self):
        pass

    def _addr_h(self):
        pass

    def _addr_l(self):
        pass

    def _addhl(self):
        pass

    def _addr_a(self):
        pass

    def _adcr_b(self):
        pass

    def _adcr_c(self):
        pass

    def _adcr_d(self):
        pass

    def _adcr_e(self):
        pass

    def _adcr_h(self):
        pass

    def _adcr_l(self):
        pass

    def _adchl(self):
        pass

    def _adcr_a(self):
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