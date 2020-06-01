from pyglet import image

BGON = 0x01    # Background on
SPON = 0x02    # Sprites on
SPSZ = 0x04    # Sprite size (0 = 8x8, 1 = 16x16)
BGMAP = 0x08   # Background map
BGSET = 0x10   # Background tileset
WINON = 0x20   # Window on
WINMAP = 0x40  # Window tilemap
DISPON = 0x80  # Display on


class GPU(object):
    """
    GPU class that handles outputting tile set to the window.
    """

    def __init__(self, mmu):
        self.mmu = mmu
        self.line = 0
        self.mode = 0
        self.mode_clock = 0
        self.reg = []
        self.scan_row = []
        pattern = image.SolidColorImagePattern(color=(255, 255, 255, 255))
        self.display = pattern.create_image(144, 160).get_image_data()

        self.color_map = {
            0: '#FFFFFF',
            1: '#AAAAAA',
            2: '#555555',
            3: '#000000',
        }

    def step(self, clock_ticks):
        """
        Single GPU drawing step.

        Essentially this should be called after every opcode to update where the
        GPU is in drawing the screen.
        Each instruction carries a gpu cycle count with it, and that change gets
        reconputed here. Depending on what stage you are in, this may call the
        screen to be redrawn (basically when we hit v-blank)

        Parameters
        ----------
        clock_ticks : int
            cpu ticks required for given step, provided by operation
        """

        self.mode_clock += clock_ticks
        if self.mode == 2:
            # OAM read mode, scanline is active
            if(self.mode_clock >= 80):
                # Enter mode 3 (VRAM read)
                self.mode_clock = 0
                self.mode = 3
        elif self.mode == 3:
            # VRAM read mode
            if self.mode_clock >= 172:
                # Enter mode 0 (h-blank)
                self.mode_clock = 0
                self.mode = 0
                # At this point write one horizontal line to the frame buffer
        elif self.mode == 0:
            # H-blank
            if self.mode_clock >= 204:
                self.mode_clock = 0
                self.line += 1
                self.mmu.mmio[0x44] += 1

                if self.line == 143:
                    # last horizontal line run, move to v-blank
                    self.mode = 1
                    self.render_screen()
                else:
                    self.mode = 2
        elif self.mode == 1:
            if self.mode_clock >= 456:
                self.mode_clock = 0
                self.line += 1

                if self.line > 153:
                    # restart scanning modes
                    self.mode = 2
                    self.line = 0

    def update(self, data, addr):
        """
        #TODO: finish function
        """
        # print('addr: ', addr)
        # print('data: ', data)
        # print(self.display.get_region(x, y, 1, 1).get_image_data())
        return None

    def render_screen(self):
        self.display.blit(0, 0)

    def __str__(self):
        return """GPU Mode: %d  Mode Clock: %d  Line: %3d (%02x)""" %
                (self.mode, self.mode_clock, self.line, self.line)

    def reset(self):
        """
        Resets all private variables to default values.
        Needed when restarting rom.
        """
        pass
