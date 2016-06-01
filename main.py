__author__ = 'cjpowell'

rom = open('gbpy/resources/test_file.gb', "rb").read()
for index in range(0, len(rom)):
    print(hex(rom[index]))
    input()
