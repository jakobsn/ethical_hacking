#!/usr/bin/python
from Crypto.PublicKey import RSA
from fractions import gcd
f = open("AlicePublickey.pem",'r')
apk = RSA.importKey(f.read())
f.close()
f = open("BobPublickey.pem",'r')
bpk = RSA.importKey(f.read())
f.close()
f = open("ciphertext",'r')
ct = f.read()
f.close()

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

mygcd = gcd(apk.n,bpk.n)

mes = '@\n\xea\xa9\xd9C6\xfd]{:\xaf\xe0\xf6\xe3\x15\xb7\x92i\x0e}\x7f\x8c\xc5\xa9q\xcb\x94\xac{\xad\x0bU\xf5\x8b\xfe\xfbd\xa2\x8e\x19\xa0\xddN\xbb\xfc\xb3W\xcez\xa3\x17\xa8U\n\xf4\xda\xc4\xe1\xa1x"Gw\x00\x12\xd9`;\n\x0c\x94\xef\xe8S\xcd\xa8\x91\xb6\xf08\xeb\n\x8d\xa9u\xec]\xd8\xeb\x98\xf7\x9c\xdbW\xe1h}h\x92\x0f\xa0\x8d\xd8\x0c\x978\xe6\xf7\xc5\xdb\xaa\xca\xf1P\xbf\x1e5\xba\x9f\rc\x92CB\x1eX\x84'
apk.q = apk.n/mygcd
bpk.q = bpk.n/mygcd

apk.l = (apk.q-1)*(mygcd-1)
bpk.l = (bpk.q-1)*(mygcd-1)

apk.d = modinv(apk.e,apk.l)
bpk.d = modinv(bpk.e,bpk.l)

akey = RSA.construct((apk.n, apk.e, apk.d))
bkey = RSA.construct((bpk.n, bpk.e, bpk.d))

print akey.decrypt(mes)
