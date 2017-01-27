# BSD 2-Clause License

# Copyright (c) 2017, xabiergarmendia@gmail.com
# All rights reserved.
#
# Code used:
# https://github.com/pajacobson/td5keygen by paul@discotd5.com
#
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




import time
import serial
from math import *
import os
import logging, sys

import sys, time, msvcrt

os.system("cls")

    # exit()
    
# trash=raw_input(inprimatu)

menu_code=0;

while (True):
    time.sleep(0.1)
    os.system("cls")
    print "-------------------------------------------------------------------------------"
    print "|                Land Rover Td5 Motorren Azterketa Programa                   |"
    print "| Port: COM3 - Auth: Done - Connection: OK - Status: NOT Immobilized          |"
    print "-------------------------------------------------------------------------------"
    print "| 1. Fuelling - 2. Inputs - 3. Outputs - 4. Settings - 5. Faults - 6. Map     |"
    print "-------------------------------------------------------------------------------"
    if (menu_code==0):
        print "\n Land Rover Td5 Motorren Azterketa Programa"
        print "\t\t Ongi Etorri"
        print ""
        print " BSD 2-Clause License"
        print " Egilea: EA2EGA - Garmen - xabiergarmendia@gmail.com"
        print " Erabilitako kodea:"
        print "\thttps://github.com/pajacobson/td5keygen"
        print "\t\tpaul@discotd5.com"
        print "\thttp://stackoverflow.com/questions/12090503"
        print "\t\thttp://stackoverflow.com/users/300783/thomas"
        print "\n"
        print " Serie Portu erabilgarriak:"

        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)

        if len(ports)>0:
             print ("\n "+str(ports[0]).split(' ')[0]+" Portua Erabiltzen ")
            # nb = input("\n Aukeratu Serie Portua ("+str(ports[0]).split(' ')[0]+"): ")
        else:
            print "\n Ez da serie porturik topatu sisteman :("
            print " Programa amaitzen"
    if (menu_code==1):
        print "| Fuelling Parameters                                                         |"
        print "|-----------------------------------------------------------------------------|"
    if (menu_code==2):
        print "| Inputs                                                         |"
        print "|-----------------------------------------------------------------------------|"
    
    
    if msvcrt.kbhit():
        menu_code = int(msvcrt.getch())
        time.sleep(0.5)



