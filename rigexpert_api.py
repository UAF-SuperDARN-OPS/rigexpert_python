# jon klein, jtklein@alaska.edu
# python API for rigexpert antenna analyzers, see https://rigexpert.com/data-exchange-with-rigexpert-antenna-analyzers/
# mit license

# You must be in the group dialout and tty to use a USB serial connection. 
# Use the following command to do so:
# sudo usermod -a -G tty $USER
# sudo usermod -a -G dialout $USER

import serial
import numpy as np

RIGPORT = '/dev/ttyUSB0'
VERBOSE = True

class rigexpert_analyzer:
    def __init__(self, port = RIGPORT):
        self.port = port
        self.ser = serial.Serial(self.port, 38400, timeout = 5)
        assert self._command_scalar('ON') == 'OK'
        #assert self._command_scalar('VER') == 'AA-30 109'
        self.span_hz = 0
        self.cfreq_hz = 0

    def open(self):
        self.ser = serial.Serial(self.port, 38400, timeout = 5)
        assert self._command_scalar('ON') == 'OK'
        self.span_hz = 0
        self.cfreq_hz = 0

    def close(self):
        assert self._command_scalar('OFF') == 'OK'
        self.ser.close()
    
    # set center frequency in hz
    def cfreq(self, freq):
        assert self._command_scalar(f"FQ{int(freq)}") == 'OK'
        self.cfreq_hz = freq
    
    # set span in hz
    def span(self, span_hz):
        assert self._command_scalar(f"SW{int(span_hz)}") == 'OK'
        self.span_hz = span_hz

    # measure a sweep
    def sweep(self, npoints):
        assert self.cfreq_hz != 0
        assert self.span_hz != 0
        assert npoints > 0

        cmd = f"FRX{int(npoints)}"

        s = self._command_vector(cmd, npoints+1)
        f = np.array([si[0] for si in s])
        r = np.array([si[1] for si in s])
        x = np.array([si[2] for si in s])
        
        return (f, r, x)

    def _command_scalar(self, cmd):
        self.ser.write((cmd + '\n').encode('utf-8'))
        r = self.ser.readline().decode()
        while len(r) == 2 : # skip ahead, the aa-30 spits out lots of blank lines..
            r = self.ser.readline().decode()
        if VERBOSE:
            print(f"command: {cmd}, response: {r}")
        return r[:-2]

    def _command_vector(self, cmd, lines):
        self.ser.write((cmd + '\n').encode('utf-8'))

        print(f"command: {cmd}")

        r = []

        for i in range(lines):
            l = self.ser.readline().decode().split(',')
            l = [float(li) for li in l]
            r.append(l)
            print( r[-1])
        
        return r



