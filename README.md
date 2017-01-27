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

* Read Fuelling: 90% Done (EGR and Wastegate to be tested)
* Read Switches: 95% Done (Auto Gearbox data is missing)
* Read/Write Settings: Not yet
* Read/Clear Faults: Not yet
* Test Outputs: Not yet
* Security Status: Not yet
* Learn Alarm Code: Not yet
* Read/Write Map: Not yet

## Land Rover Td5 Storm Engine ECU OBD-II Protocol

### Introduction

The Land Rover Td5 Storm engine ECUs, have diagnostic capabilities via the OBD-II port. This system mainly allows the reading of fuelling parameters, reading input switches, checking outputs, reading and clearing faults, reading and writting ECU settings (Injector types, accelerator type, security code learning), and in NNN type ECUs, reflashing.

The ECU communicates with the diagnostic equipment using the ISO 9141-2 protocol, using the K-Line as phisical layer.

### Initialization

To start a diagnostic session, the diagnostic system does a Fast Init as described in the ISO 9141-2, holding the K-Line low during 25ms.

After that it sends a initialization frame, a diagnostics start request, a 