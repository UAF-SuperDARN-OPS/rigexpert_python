#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import csv
import pdb

from rigexpert_api import rigexpert_analyzer

def main():
    radar = input("Enter the site name: ")
    ant = input("Enter an antenna number [0-99]: ")
    start_freq = float(input("Enter start frequency [MHz]: "))
    stop_freq = float(input("Enter stop frequency [MHz]: "))

    center_freq = (stop_freq + start_freq) / 2
    print(f"Center frequency: {center_freq} MHz")
    span = stop_freq - start_freq
    print(f"Span: {span} MHz")

    ra = rigexpert_analyzer()
    ra.cfreq(center_freq * 1e6)
    ra.span(span * 1e6)
    f, r, x = ra.sweep(int(span * 20))

    ra.close()
    
    z = r + 1j * x
    z0 = 50
    ref = abs((z - z0) / (z + z0))
    vswr = (1 + ref) / (1 - ref)
   
    
    with open(f"{radar}_ant{int(ant):02}.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(["Freq (MHz)", "VSWR", "R (ohms)", "X (ohms)"])
        for i in range(len(f)):
            csvwriter.writerow([f[i], vswr[i], r[i], x[i]])

    print(f)
    plt.plot(f, vswr)
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("VSWR")
    plt.title(f"Antenna {ant} VSWR")
    plt.yticks(np.arange(0, 11, step=1))
    axes = plt.gca()
    axes.set_ylim([0, 10])
    axes.grid(True)
    plt.savefig(f"{radar}_ant{int(ant):02}.png") 
    plt.show()
    
if __name__ == '__main__':
    main()
