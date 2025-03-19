"""
Programme de test du FPGA
"""

import serial
from ascon_pcsn import *

port = "COM4"

ser = serial.Serial(port, 115200, timeout=1)

# commandes
KEY =   bytes.fromhex('4C8A55114D1CB6A9A2BE263D4D7AECAAFF')
NONCE = bytes.fromhex('4F4ED0EC0B98C529B7C8CDDF37BCD0284A')
DA =    bytes.fromhex('424120746F20428000')
WAVE =  bytes.fromhex('585A5B5B5A5A5A5A5A59554E4A4C4F545553515354565758575A5A595756595B5A5554545252504F4F4C4C4D4D4A49444447474644424341403B36383E4449494747464644434243454745444546474A494745484F58697C92AECEEDFFFFE3B47C471600041729363C3F3E40414141403F3F403F3E3B3A3B3E3D3E3C393C41464646454447464A4C4F4C505555524F5155595C5A595A5C5C5B5959575351504F4F53575A5C5A5B5D5E6060615F605F5E5A5857545252800000')
GO =    bytes.fromhex('48')
TAG =   bytes.fromhex('55')
CIPHER =bytes.fromhex('44')

print(KEY[1:])
print(NONCE[1:])
print(DA[1:])

# envoi des commandes
print("Send KEY...")
ser.write(KEY)
print(ser.read(3))

print("Send NONCE...")
ser.write(NONCE)
print(ser.read(3))

print("Send DA...")
ser.write(DA)
print(ser.read(3))

print("Send WAVE...")
ser.write(WAVE)
print(ser.read(3))

print("Send GO...")
ser.write(GO)
print(ser.read(3))
# réception des données

print("Wait for cipher...")
ser.write(CIPHER)
cipher = ser.read(184)
print(cipher)
print(ser.read(3))

print("Wait for tag...")
ser.write(TAG)
tag = ser.read(16)
print(tag)
print(ser.read(3))

print("Tailler cipher: ", len(cipher))
print("Tailler tag: ", len(tag))
# decodage

# print(len(cipher[:-3]))

plain = ascon_decrypt(KEY[1:], NONCE[1:], DA[1:-2], cipher[:-3]+tag)
print(plain)