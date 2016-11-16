from register import Register


class Registers(object):
    def __init__(self):
        self.sp = Register(0xfffe, limit=0xffff)
        self.pc = Register(0x100, limit=0xffff)

        self.a = Register(0x1)
        self.b = Register(0)
        self.c = Register(0x13)
        self.d = Register(0)
        self.e = Register(0xd8)
        self.h = Register(0x1)
        self.l = Register(0x4d)

        self.zero_flag = 1
        self.sub_flag = 0
        self.hc_flag = 1
        self.carry_flag = 1

    def jump(self, value):
        self.pc = Register(value)

    def flags(self):
        # TODO: Need to return flags 'register'
        pass