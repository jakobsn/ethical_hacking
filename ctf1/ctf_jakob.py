#!/usr/bin/python2.7

from Crypto.PublicKey import RSA

f = open('AlicePublickey.pem', 'r')
AlicePublicKey = RSA.importKey(f.read())
f.close()

f = open('BobPublickey.pem', 'r')
BobPublicKey = RSA.importKey(f.read())
f.close()

print AlicePublicKey.n
print BobPublicKey.n

