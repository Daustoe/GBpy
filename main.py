__author__ = 'cjpowell'

rom = open('resources/test_file.gb', "rb").read()
for index in range(0, len(rom)):
    print(hex(index), ': ', hex(rom[index]))
    input()

# 41: 24
# 42: 20