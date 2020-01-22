RigExpert Antenna Analyzer
==========================

This suite of software uses the RigExpert AA-30 to do useful field measurements.

VSWR
====
Run the 'measure_vswr.py' script. It will prompt you for the site name, antenna number, start and stop frequencies (in MHz). Points are gathered at 20 points per MHz. The data is stored to a CSV file and the VSWR plot is saved as a PNG.

Cable Length of Distance to Fault
=================================
Run the 'cable_length_or_fault.py' script. This script approximates the length of an unterminated cable. The approximate value may differ from the actual value, but that is a result of actual velocity of propagation differing slightly from the value provided by the manufacture. The returned distance is either the length of the cable or the distance to a fault. Currently, there is no way to distinguish between a fault or the end of a cable, as both are opens.

RigExpert API
=============
The 'rigexpert_api.py' file contains the commands to interface with the RigExpert over a USB connection. The commands are based on the commands provided by RigExpert, which can be viewed in the 'AA30-commands.txt' file.
