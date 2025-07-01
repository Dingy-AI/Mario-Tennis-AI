from pyboy import PyBoy
pyboy = PyBoy('smbd.gbc')
while pyboy.tick():
    print(pyboy.memory[0xC1C1])

    pass

pyboy.stop()