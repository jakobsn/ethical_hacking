#!/usr/bin/python
from Crypto.Cipher import AES
import binascii

ciphertext = ""

with open("Workbook.xlsx.enc","rb") as file:
    raw = file.read()
    hex1 = (binascii.hexlify(raw))

with open("AttackAtTheDawn.txt.enc","rb") as file:
    raw2 = file.read()
    hex2 = binascii.hexlify(raw2)


def strxor(a, b):
    if len(a) > len(b):
        return '%x' % (int(a[:len(b)],16)^int(b,16))
    else:
        return '%x' % (int(a,16)^int(b[:len(a)],16))
"""
i = 0
with open("dump.txt", "w") as f:
    while True:
        if i*32 > len(hex1):
            break
        f.write(strxor(hex2, hex1[i*32:]).decode("hex"))
        i+= 1
"""

print(strxor(hex2, hex1[8*32:]).decode("hex"))
