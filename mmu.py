"""
Memory management unit for the GameBoy emulator.
Note that the Video RAM (GRAPHICS RAM) is handled by the gpu, not the mmu. This was not the case really in the GameBoy,
but it will simplify the organization of this program.

From a technical standpoint, the only four operations that the GameBoy CPU cares about are readWord, readByte,
writeWord, and writeByte. With these four functions the CPU can run it's full opcode list.
"""
__author__ = 'Clayton Powell'


class MMU(object):
    """
    MMU class that handles memory operations for the GameBoy emulator.
    """

    def __init__(self):
        self.bios = [0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
                     0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
                     0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
                     0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
                     0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
                     0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
                     0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
                     0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
                     0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
                     0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
                     0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
                     0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
                     0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
                     0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
                     0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
                     0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50]
        self.rom = []
        self.wram = []
        self.eram = []
        self.zram = []
        self.mmio = []
        self.interrupt_enable = 0
        self.reset()

    def reset(self):
        """
        Resets memory to initial values
        :return:
        """
        self.rom = [0] * 0x4000
        self.wram = [0] * 0x2000
        self.eram = [0] * 0x8000
        self.zram = [0] * 0x80
        self.mmio = [0] * 0x80
        self.interrupt_enable = 0

    def load(self, rom_path):
        """
        Loads the rom at the given rom_path into local memory.
        :param rom_path:
        """
        self.reset()
        rom = open(rom_path, "rb").read()
        for index in range(0, len(self.rom)):
            self.rom[index] = rom[index]

    def write_byte(self, addr, value):
        """
        Writes a byte (8 bit) value to the address specified.
        :param addr:
        :param value:
        """
        if addr >= 0xff80:
            # Zero page RAM
            if addr == 0xffff:
                self.interrupt_enable = value
            else:
                self.zram[addr & 0x7f] = value
        elif addr >= 0xff00:
            # MMIO is a funny thing, needs looking into.
            pass
        elif addr >= 0xfea0:
            # unused space
            pass
        elif addr >= 0xfe00:
            # Object Attribute Memory (OAM) in gpu
            # TODO implement this in gpu: return self.gpu.oam[addr & 0xff]
            pass
        elif addr >= 0xe000:
            # Working RAM shadow (read wram anyway)
            self.wram[addr & 0x1fff] = value
        elif addr >= 0xc000:
            # Working RAM main
            self.wram[addr & 0x1fff] = value
        elif addr >= 0xa000:
            # External RAM
            #TODO need to implement memory bank controllers for this,
            pass
        elif addr >= 0x8000:
            # Graphics RAM
            # TODO implement this in gpu: return
            # return self.gpu.vram[addr & 0x1fff]
            pass
        elif addr >= 0x4000:
            # ROM Bank 1
            # TODO implement memory bank controllers to enable this
            pass
        else:
            # ROM Bank 0
            self.rom[addr] = value

    def write_word(self, addr, value):
        """
        Writes a word (16 bit) value to the address specified.
        :param addr:
        :param value:
        """
        self.write_byte(addr, value & 0xff)
        self.write_byte(addr + 1, value >> 8)

    def read_byte(self, addr):
        """
        Reads a single 8 bit value from the address specified.
        :param addr:
        :return:
        """
        if addr >= 0xff80:
            # Zero page RAM
            if addr == 0xffff:
                return self.interrupt_enable
            else:
                return self.zram[addr & 0x7f]
        elif addr >= 0xff00:
            # MMIO
            return self.mmio[addr & 0xff]
        elif addr >= 0xfea0:
            # unused space
            return 0
        elif addr >= 0xfe00:
            # Object Attribute Memory (OAM) in gpu
            # TODO implement this in gpu: return self.gpu.oam[addr & 0xff]
            pass
        elif addr >= 0xe000:
            # Working RAM shadow (read wram anyway)
            return self.wram[addr & 0x1fff]
        elif addr >= 0xc000:
            # Working RAM main
            return self.wram[addr & 0x1fff]
        elif addr >= 0xa000:
            # External RAM
            #TODO need to implement memory bank controllers for this,
            pass
        elif addr >= 0x8000:
            # Graphics RAM
            # TODO implement this in gpu: return
            # return self.gpu.vram[addr & 0x1fff]
            pass
        elif addr >= 0x4000:
            # ROM Bank 1
            # TODO implement memory bank controllers to enable this
            pass
        else:
            # ROM Bank 0
            return self.rom[addr]

    def read_word(self, addr):
        """
        Reads a 16 bit word value from the address specified.
        :param addr:
        :return:
        """
        return self.read_byte(addr) + (self.read_byte(addr + 1) << 8)

    # TODO implement write functions
