#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import csv
import pdb

from rigexpert_api import rigexpert_analyzer

RADAR = 'ionosonde'

def main():
    ant = input('Enter an antenna number: ')
    ra = rigexpert_analyzer()
    ra.cfreq(10e6)
    ra.span(20e6)
    f, r, x = ra.sweep(400)

    ra.close()
    
    z = r + 1j * x
    z0 = 50
    ref = abs((z - z0) / (z + z0))
    vswr = (1 + ref) / (1 - ref)
   
    
    with open(f"{RADAR}_ant{int(ant):02}.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(['Freq (MHz)', 'VSWR', 'R (ohms)', 'X (ohms)'])
        for i in range(len(f)):
            csvwriter.writerow([f[i], vswr[i], r[i], x[i]])

    print(f)
    plt.plot(f, vswr)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('VSWR')
    plt.title(f"Antenna {ant} VSWR")
    plt.yticks(np.arange(0, 11, step=1))
    axes = plt.gca()
    axes.set_ylim([0, 10])
    axes.grid(True)
    plt.savefig(f"{RADAR}_ant{int(ant):02}.png") 
    plt.show()
    
if __name__ == '__main__':
    main()
