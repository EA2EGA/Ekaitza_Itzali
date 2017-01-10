# Ekaitza_Itzali
Land Rover Td5 Engine Disgnostic Tool

by EA2EGA

## Circuit

``Must be used with a CP2102 USB to TTL converter.
The CP2102 must be set up for 360 bauds instead of 300
and 10400 bauds instead of 14400.
This can be done with the AN205SW tool from Silicon Labs,
the manufacturer of the CP2102

Schematic:

        Car Obd Port       |       CP2102 USB to TTL converter
                           |
K-line      12 Volt   GND  |  GND   5 Volt    RX        TX
 |           |         |       |     |         |        |
 |           |         |-------|     |         |        |
 |           |                       |         |        |
 |--2K2------|       Reduce signal   |         |        |
 |                         to 0-5V   |         |        |
 |--22K--------1N4184->--------------|         |        |
 |        |                                    |        |
 |        |----------2K2-----------------------|        |
 |                                                      |
 |                                                      |
 |     2N2222A              (Invert again and Power)    |
 |     C  B  E                                          |
 |     |  |  |-------GND                                |
 |------  |                                             |
          |                                             |
          |--------|                                    |
                   |                                    |
      5 Volt       |  2N2222A      (Inverter)           |
         |-----2K2----C  B  E                           |
                         |  |----- GND                  |
                         |                              |
                         |------------------2K2---------|
``
