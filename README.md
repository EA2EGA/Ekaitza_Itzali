# Ekaitza_Itzali
Land Rover Td5 Engine Disgnostic Tool

by EA2EGA

Must be used with a CP2102 USB to TTL converter.
The CP2102 must be set up for 360 bauds instead of 300
and 10400 bauds instead of 14400.
This can be done with the AN205SW tool from Silicon Labs,
the manufacturer of the CP2102

## Credits

This work would had been impossible withouth the work of OffTrack and the work of Luca72.

### ECU Authentification algorithm

A awsome work have been made by OffTrack, dissasembling the ECU code. One part of it is the ECU authentification algorithm: https://github.com/pajacobson/td5keygen

### Td5Opencom

Luca72 did a diagnostic system based on a Arduino Mega2650. Which had been very valious, since it had saved me a lot of time of reverse engineering: http://luca72.xoom.it/td5mapsuiteweb/archive/td5opencom/

## List of Features:

* Read Fuelling: 110% Done (EGR and Wastegate to be tested, but getting more params than the Nanocom)
* Read Switches: 95% Done (Auto Gearbox data is missing)
* Read/Write Settings: 30% Done (Read VIN, fuel and map variants and VIN)
* Read/Clear Faults: 100% Done
* Test Outputs: 100% Done
* Security Status: Not yet
* Learn Alarm Code: Not yet
* Read/Write Map: 50% (Reading maps achieved)

* Serve fuelling data via JSON: 0%

## Land Rover Td5 Storm Engine ECU OBD-II Protocol

### Introduction

The Land Rover Td5 Storm engine ECUs, have diagnostic capabilities via the OBD-II port. This system mainly allows the reading of fuelling parameters, reading input switches, checking outputs, reading and clearing faults, reading and writting ECU settings (Injector types, accelerator type, security code learning), and in NNN type ECUs, reflashing.

The ECU communicates with the diagnostic equipment using the ISO 9141-2 protocol, using the K-Line as phisical layer.

### Initialization

To start a diagnostic session, the diagnostic system does a Fast Init as described in the ISO 9141-2, holding the K-Line low during 25ms. After that it sends a initialization frame, a diagnostics start request, and a authentification Seed request. The ECU answers with a Seed, and the diagnostic system has to answer with the correct Key. If a correct key is sent, the ECU answers with a Auth OK message, and allows to read its parameters.

The Seed-Key can be get using the td5keygen code.

Here you can see the initialization process. The last byte, between parhentesis, is the checksum
```
Diag: 25ms Low
Diag: 25ms High
Diag: Switch to 10400 Baud
Diag: 0x81 0x13 0xf7 0x81 (0x0c)                   Init Frame
ECU : 0x03 0xc1 0x57 0x8f (0xaa)
Diag: 0x02 0x10 0xa0 (0xb2)                        Start Diagnostics
ECU : 0x01 0x50 (0x51)
Diag: 0x02 0x27 0x01 (0x2a)                        Seed Request
ECU : 0x04 0x67 0x01 [Seed_L] [Seed_H] (0x62)      Seed Answer
Diag: 0x04 0x27 0x02 [Key_L]  [Key_H]  (0x43)      Key Response
ECU : 0x02 0x67 0x02 (0x6b)                        Auth Ok!
```