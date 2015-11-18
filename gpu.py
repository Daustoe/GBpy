class GPU(object):
    """
    GPU class that handles outputting tile set to the window.
    """

    def __init__(self):
        self.vram = []
        self.oam = []
        self.reg = []
        self.tilemap = []
        self.scanrow = []

    def reset(self):
        """
        Resets all private variables to default values. Needed when restarting rom.
        """
        self.vram = [0 for index in range(0, 0x2000)]
        self.oam = [0 for index in range(0, 160)]