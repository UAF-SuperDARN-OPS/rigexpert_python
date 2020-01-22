
import numpy as np
import matplotlib.pyplot as plt
import csv
import pdb

from rigexpert_api import rigexpert_analyzer

def main():
    velocity_factor = 0.66
    c = 299792458
    cable_velocity = c * velocity_factor

    resonance_frequency = 15

    ra = rigexpert_analyzer()
    ra.close()

    for approx in range(4):
        ra.open()
        ra.cfreq(resonance_frequency * 1e6)
        ra.span(30e6 / 10**(approx))
        f, r, x = ra.sweep(10)

        ra.close()

        for value in range(len(x)):
            if (x[value] * x[value + 1]) <= 0:
                resonance_frequency = (f[value] + f[value + 1]) / 2
                break
        print(f"Resonance of approximation {approx}: {resonance_frequency * 1e6}")

    
    print(f"Final resonance approximation: {resonance_frequency * 1e6}")
    print(f"Cable length or length of fault is: {cable_velocity / (resonance_frequency * 1e6) * (1/4):.2f} m")
    
    
if __name__ == '__main__':
    main()
