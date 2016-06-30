__author__ = 'Clayton Powell'
import gbpy
import pyglet
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=str, help="File path to the GameBoy Rom you wish to run.")
    args = parser.parse_args()
    template = pyglet.gl.Config(double_buffer=False)
    emulator = gbpy.Gbpy(160, 144, config=template, caption="GameBoy Emulator")
    pyglet.app.run()