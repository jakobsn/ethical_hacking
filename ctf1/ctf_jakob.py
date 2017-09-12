#!/usr/bin/python2.7

from Crypto.PublicKey import RSA
import numpy
import fractions

f = open('AlicePublickey.pem', 'r')
AlicePublicKey = RSA.importKey(f.read())
f.close()

f = open('BobPublickey.pem', 'r')
BobPublicKey = RSA.importKey(f.read())
f.close()

print AlicePublicKey.n
print BobPublicKey.n

gcd = fractions.gcd(BobPublicKey.n, AlicePublicKey.n)

print "gcd:", gcd