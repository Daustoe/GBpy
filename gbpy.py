__author__ = 'Clayton Powell'
import cpu
import mmu
import gpu
import pyglet


class Gbpy(pyglet.window.Window):
    """
    GameBoy Py emulator class. Subclasses pyglet Window class and contains the
    cpu, gpu, and mmu of the GB interpreter.
    """

    def __init__(self, *args, **kwargs):
        super(Gbpy, self).__init__(*args, **kwargs)
        self.mmu = mmu.MMU()
        self.gpu = gpu.GPU(self.mmu)
        self.cpu = cpu.Cpu(self.mmu)
        self.clear()
        self.set_vsync(False)

    def load_rom(self, rom_path):
        """
        Hand off to mmu to load the rom into memory from file at rom_path.
        :param rom_path:
            Path to ROM on system
        """
        self.mmu.load(rom_path)

    def main(self):
        """
        Main loop of the emulator. Handles keyboard events and cpu cycle.
        :param dt:
            time delta, used because this is a scheduled function
        """
        if not self.has_exit:
            self.dispatch_events()
            cycles = self.cpu.cycle()
            self.gpu.step(cycles)


    def on_key_press(self, symbol, modifiers):
        """

        :param symbol:
        :param modifiers:
        :return:
        """
        pass

    def on_key_release(self, symbol, modifiers):
        """

        :param symbol:
        :param modifiers:
        :return:
        """
        pass
