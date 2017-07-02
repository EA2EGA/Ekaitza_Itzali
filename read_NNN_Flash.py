# BSD 2-Clause License

# Copyright (c) 2017, xabiergarmendia@gmail.com
# All rights reserved.
#
# Code used:
# https://github.com/pajacobson/td5keygen by paul@discotd5.com

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
  # list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
  # this list of conditions and the following disclaimer in the documentation
  # and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Ekaitza Itzali
# by EA2EGA
#
# Must be used with a CP2102 USB to TTL converter.
# The CP2102 must be set up for 360 bauds instead of 300
# and 10400 bauds instead of 14400.
# This can be done with the AN205SW tool from Silicon Labs,
# the manufacturer of the CP2102
#
# Schematic:
#
# The first version of the circuit had poor noise inmunity
# This version have changed some resistance values and added a 
# high frecuency noise filtering capacitor.
# No the number of chesum errors is negligible.
#
#         Car Obd Port       |       CP2102 USB to TTL converter
#                            |
# K-line      12 Volt   GND  |  GND   5 Volt    RX        TX
#  |           |         |       |     |         |        |
#  |           |     |---|-------|     |         |        |
#  |           |     |                 |         |        |
#  |--510------|     | Reduce signal   |         |        |
#  |                 |       to 0-5V   |         |        |
#  |        |--100pF-|             |         |        |
#  |        |                          |         |        |
#  |--2K2--------1N4184->--------------|         |        |
#  |        |                                    |        |
#  |        |------------------------------------|        |
#  |                                                      |
#  |                                                      |
#  |     2N2222A              (Invert again and Power)    |
#  |     C  B  E                                          |
#  |     |  |  |-------GND                                |
#  |------  |                                             |
#           |                                             |
#           |--------|                                    |
#                    |                                    |
#       5 Volt       |  2N2222A      (Inverter)           |
#          |-----2K2----C  B  E                           |
#                          |  |----- GND                  |
#                          |                              |
#                          |------------------2K2---------|


import time
import serial
from math import *
import os
import logging, sys
import msvcrt
from pyftdi.ftdi import Ftdi
import binascii

debug = 5
interframe_delay=0.002
serial_port = 'COM3'

def fast_init():
    #ser = serial.Serial(serial_port, 360, timeout=0.1) #CP210x is configured for 300 being 360
    ser = serial.Serial(serial_port, 360, timeout=0.1)
    command=b"\x00"
    ser.write(command) #Send a 25ms pulse
    time.sleep(0.025)
    ser.close()

def send_packet(data,res_size):
    global debug
    time.sleep(interframe_delay)
    
    lendata=len(data)
    modulo=0
    for i in range(0,lendata):
        modulo = modulo + data[i]
    modulo = modulo % 256
    to_send=data+chr(modulo).encode('latin1')
    ser.write(to_send)
    time.sleep(interframe_delay)

    ignore=len(to_send)
    read_val = ser.read(len(to_send)+res_size)

    read_val_s = read_val[0:ignore]
    if debug > 2:    
        print ("Data Sent: %s." % binascii.b2a_hex(read_val_s))
    read_val_r = read_val[ignore:]
    if debug > 2: 
        print ("Data Received: %s." % binascii.b2a_hex(read_val_r))
    
    modulo=0
    for i in range(0,len(read_val_r)-1):
        modulo = modulo + read_val_r[i] 
    modulo = modulo % 256
    
    if (len(read_val_r)>2):
        if (modulo!=read_val_r[len(read_val_r)-1]): #Checksum error
            read_val_r=""
            if debug > 1:
                print ("Checksum ERROR")
       
    return read_val_r

def seed_key(read_val_r):
    seed = read_val_r[3:5]
    if debug > 1:
        print ("\tSeed is: %s." % binascii.b2a_hex(seed))
    seed_int=seed[0]*256+seed[1]
    if debug > 1:
        print ("\tSeed integer: %s." % seed_int)
    
    seed=seed_int

    count = ((seed >> 0xC & 0x8) + (seed >> 0x5 & 0x4) + (seed >> 0x3 & 0x2) + (seed & 0x1)) + 1

    idx = 0
    while (idx < count):
            tap = ((seed >> 1) ^ (seed >> 2 ) ^ (seed >> 8 ) ^ (seed >> 9)) & 1
            tmp = (seed >> 1) | ( tap << 0xF)
            if (seed >> 0x3 & 1) and (seed >> 0xD & 1):
                    seed = tmp & ~1
            else:
                    seed = tmp | 1

            idx = idx + 1

    if (seed<256):
        high=0x00
        low=seed
    else:
        high=seed/256
        low=seed%256

    key=chr(int(high)).encode('latin1')+chr(int(low)).encode('latin1')
    if debug > 1:
        print ("\tKey hex: %s." % binascii.b2a_hex(key))
        
    key_answer=b"\x04\x27\x02"+chr(int(high)).encode('latin1')+chr(int(low)).encode('latin1')
    
    return key_answer
    
def initialize():
    global ser
    fast_init()

    ser = serial.Serial(serial_port, 10400, timeout=0.1)    #CP210x must be configured for 

    time.sleep(0.1)
    response=send_packet(b"\x81\x13\xF7\x81",5)             #Init Frame
    time.sleep(0.1)
    response=send_packet(b"\x02\x10\xA0",3)             #Start Diagnostics
    time.sleep(0.1)
    response=send_packet(b"\x02\x27\x01",6)             #Seed Request

    if (len(response)==6):
        key_ans=seed_key(response)
        response=send_packet(key_ans,4)             #Seed Request

    time.sleep(0.2)
    
initialize()

print ("\n\tLand Rover Td5 Map Reader\n")

f=open('outputfile.bin', 'wb')

byte1=0x11
byte2=0x00
byte3=0x00
while (1):

    percent=((byte1-0x11)*256*256+byte2*256+byte3)/(3*256*256)
    address=bytes([byte1])+bytes([byte2])+bytes([byte3])
    print("\tReading Address: %s - %s Complete" % (binascii.b2a_hex(address),'{:.1%}'.format(percent)), end="\r")

    if (byte1==0x13 and byte2==0xff):
        response=send_packet(b"\x05\x23"+bytes([byte1])+bytes([byte2])+bytes([byte3])+b"\x10",20)
        while (len(response)<19):
            response=send_packet(b"\x05\x23"+bytes([byte1])+bytes([byte2])+bytes([byte3])+b"\x10",20)
        f.write(response[3:19])
    else:
        response=send_packet(b"\x05\x23"+bytes([byte1])+bytes([byte2])+bytes([byte3])+b"\x40",68)
        while (len(response)<67):
            response=send_packet(b"\x05\x23"+bytes([byte1])+bytes([byte2])+bytes([byte3])+b"\x40",68)
        f.write(response[3:67])
    
    if (byte1==0x13 and byte2==0xff and byte3==0xe0):
        break

    if (byte1==0x13 and byte2==0xff):
        byte3=byte3+0x10
    else:
        byte3=byte3+0x40
        
    if byte3==256:
        byte2=byte2+1
        byte3=0
        if byte2==256:
            byte1=byte1+1
            byte2=0

f.close()
