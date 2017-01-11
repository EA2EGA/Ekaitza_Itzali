# BSD 2-Clause License

# Copyright (c) 2017, xabiergarmendia@gmail.com
# All rights reserved.

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
#         Car Obd Port       |       CP2102 USB to TTL converter
#                            |
# K-line      12 Volt   GND  |  GND   5 Volt    RX        TX
#  |           |         |       |     |         |        |
#  |           |         |-------|     |         |        |
#  |           |                       |         |        |
#  |--2K2------|       Reduce signal   |         |        |
#  |                         to 0-5V   |         |        |
#  |--22K--------1N4184->--------------|         |        |
#  |        |                                    |        |
#  |        |----------2K2-----------------------|        |
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

debug = 5;
serial_port = 'COM3'

def fast_init():
    ser = serial.Serial(serial_port, 300, timeout=0.1) #CP210x is configured for 300 being 360
    command=b"\x00"
    ser.write(command) #Send a 25ms pulse
    time.sleep(0.05)
    ser.close()

def send_packet(data,res_size):
    lendata=len(data)
    
    modulo=0
    for i in range(0,lendata):
        modulo = modulo + ord(data[i]) 
    modulo = modulo % 256
    
    to_send=data+chr(modulo)
    ser.write(to_send)
    time.sleep(0.01)

    ignore=len(to_send)
    read_val = ser.read(len(to_send)+res_size)

    read_val_s = read_val[0:ignore]
    if debug > 1:    
        print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
    read_val_r = read_val[ignore:]
    if debug > 1: 
        print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)
    
    return read_val_r

def seed_key(read_val_r):
    seed = read_val_r[3:5]
    if debug > 1:
        print "\tSeed is: %s." % ":".join("{:02x}".format(ord(c)) for c in seed)
    seed_int=ord(seed[0])*256+ord(seed[1])
    if debug > 1:
        print "\tSeed integer: %s." % seed_int

    counter=0

    key=[]

    with open("key.txt") as f:
        for line in f:
            if (counter==seed_int):
                content = int(line,16)
                if debug > 1:
                    print "\tKey integer: %s." % content
                hex_1=int(line[0:2],16)
                hex_2=int(line[2:4],16)
                key=chr(hex_1)+chr(hex_2)
                if debug > 1:
                    print "\tKey hex: %s." % ":".join("{:02x}".format(ord(c)) for c in key)
            
            
            counter=counter+1
    
    key_answer=b"\x04\x27\x02"+key
    return key_answer

def get_rpm():
    response=send_packet(b"\x02\x21\x09",6)
    if len(response)<6:
        rpm=0
    else:
        rpm=ord(response[3])*256+ord(response[4])
    
    return rpm
    
def get_bvolt():
    response=send_packet(b"\x02\x21\x10",8)
    if len(response)<8:
        b_voltage=0
    else:
        b_voltage=ord(response[3])*256+ord(response[4])
    
    b_voltage=float(b_voltage)/1000
    
    return b_voltage
    
    
    
    
os.system("cls")
print ""
print ""
print "\t\t Land Rover Td5 Storm - Dignostic tool"
print ""
print "Initing..."
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

time.sleep(0.1)
response=send_packet(b"\x02\x21\x02",15)             #Start Diagnostics

time.sleep(2)

debug=0

#Start requesting data
while (True):
    time.sleep(0.01)
    b_voltage=get_bvolt()
    
    time.sleep(0.01) 
    rpm=get_rpm()
    
    os.system("cls")
    print "\t\t Td5 Storm"
    print " "
    print "\t Voltaje de bateria: ", str(b_voltage)
    print "\t RPM: ", str(rpm)


ser.close()

