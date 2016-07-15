__author__ = 'Clayton Powell'
import cpu
import mmu
import gpu
import pyglet


class Gbpy(pyglet.window.Window):
    """
    GameBoy Py emulator class. Subclasses pyglet Window class and contains the cpu, gpu, and mmu of the GB interpreter.
    """

    def __init__(self, *args, **kwargs):
        super(Gbpy, self).__init__(*args, **kwargs)
        self.mmu = mmu.MMU()
        self.cpu = cpu.Cpu(self.mmu)
        self.gpu = gpu.GPU(self.mmu)
        self.clear()
        self.set_vsync(False)

    def load_rom(self, rom_path):
        """
        hands off to mmu to load the given rom.
        :param rom_path:
        :return:
        """
        self.mmu.load(rom_path)

    def main(self, dt):
        """
        Main loop of the emulator. Handles keyboard events and cpu cycle.
        :param dt:
            time delta, used because this is a scheduled function
        """
        if not self.has_exit:
            self.dispatch_events()
            self.cpu.cycle()
            self.gpu.update('temp addr', 'temp data')

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