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
        self.display = image.create(144, 160)
        self.tilemap = [0] * 144
        for each in range(144):
            self.tilemap[each] = [0x0] * 160

        self.color_map = {
            0: '#FFFFFF',
            1: '#AAAAAA',
            2: '#555555',
            3: '#000000',
        }

    def update(self, data, addr):
        print('addr: ', addr)
        print('data: ', data)
        print(self.display.get_region(x, y, 1, 1).get_image_data())
        return None

    def __str__(self):
        return """GPU Mode: %d  Mode Clock: %d  Line: %3d (%02x)""" % (self.mode, self.mode_clock, self.line, self.line)

    def reset(self):
        """
        Resets all private variables to default values. Needed when restarting rom.
        """
        pass