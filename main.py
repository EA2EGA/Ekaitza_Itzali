


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
    read_val = ser.read(len(tosend)+res_size)

    read_val_s = read_val[0:ignore]
    if debug > 1:    
        print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
    read_val_r = read_val[ignore:]
    if debug > 1: 
        print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)
    
    return read_val_r
    
os.system("cls")
print ""
print ""
print "\t\t Land Rover Td5 Storm - Dignostic tool"
print ""
print "Initing..."
fast_init()

ser = serial.Serial(serial_port, 10400, timeout=0.1) #CP210x is configured

# Init Frame
init1=b"\x81\x13\xF7\x81\x0C" 
ser.write(init1)
time.sleep(0.01)

ignore=len(init1)
read_val = ser.read(size=15)

read_val_s = read_val[0:ignore]
print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
read_val_r = read_val[ignore:]
print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)

#Start Diagnostics
init1=b"\x02\x10\xA0\xB2"
ser.write(init1)
time.sleep(0.01)

ignore=len(init1)
read_val = ser.read(size=15)

read_val_s = read_val[0:ignore]
print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
read_val_r = read_val[ignore:]
print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)

#Seed Req
init1=b"\x02\x27\x01\x2A"
ser.write(init1)
time.sleep(0.01)

ignore=len(init1)
read_val = ser.read(size=15)

read_val_s = read_val[0:ignore]
print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
read_val_r = read_val[ignore:]
print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)
seed = read_val_r[3:5]
print "\tSeed is: %s." % ":".join("{:02x}".format(ord(c)) for c in seed)
seed_int=ord(seed[0])*256+ord(seed[1])
print "\tSeed integer: %s." % seed_int

counter=0

key=[]

with open("key.txt") as f:
    for line in f:
        if (counter==seed_int):
            content = int(line,16)
            print "\tKey integer: %s." % content
            hex_1=int(line[0:2],16)
            hex_2=int(line[2:4],16)
            key=chr(hex_1)+chr(hex_2)
            print "\tKey hex: %s." % ":".join("{:02x}".format(ord(c)) for c in key)
        
        
        counter=counter+1

modulo = (int('0x04',16) + int('0x27',16) +int('0x02',16) + ord(key[0]) + ord(key[1])) %256;
        
#Key Send
init1=b"\x04\x27\x02"+key+chr(modulo)
ser.write(init1)
time.sleep(0.01)

ignore=len(init1)
read_val = ser.read(size=15)

read_val_s = read_val[0:ignore]
print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
read_val_r = read_val[ignore:]
print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)

#Start fuelling request
modulo = (int('0x02',16) + int('0x21',16) +int('0x02',16)) %256;
    
init1=b"\x02\x21\x02"+chr(modulo)
ser.write(init1)
time.sleep(0.01)

ignore=len(init1)
read_val = ser.read(size=15)

read_val_s = read_val[0:ignore]
print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
read_val_r = read_val[ignore:]
print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)

time.sleep(2)


#Start requesting data
while (True):
    time.sleep(0.01)
    modulo = (int('0x02',16) + int('0x21',16) +int('0x10',16)) %256;
    
    init1=b"\x02\x21\x10"+chr(modulo)
    ser.write(init1)
    time.sleep(0.01)

    ignore=len(init1)
    read_val = ser.read(size=12)

    read_val_s = read_val[0:ignore]
    #print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
    read_val_r = read_val[ignore:]
    #print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)
    
    b_voltage=ord(read_val_r[3])*256+ord(read_val_r[4])
    
    time.sleep(0.01)
    modulo = (int('0x02',16) + int('0x21',16) +int('0x09',16)) %256;
    
    init1=b"\x02\x21\x09"+chr(modulo)
    ser.write(init1)
    time.sleep(0.01)

    ignore=len(init1)
    read_val = ser.read(size=10)

    read_val_s = read_val[0:ignore]
    #print "Data Sent: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_s)
    read_val_r = read_val[ignore:]
    #print "Data Received: %s." % ":".join("{:02x}".format(ord(c)) for c in read_val_r)
    
    rpm=ord(read_val_r[3])*256+ord(read_val_r[4])
    os.system("cls")
    print "\t\t Td5 Storm"
    print " "
    print "\t Voltaje de bateria: ", str(float(b_voltage)/1000)
    print "\t RPM: ", str(rpm)


ser.close()

