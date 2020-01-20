
import numpy as np
import matplotlib.pyplot as plt
import csv
import pdb

from rigexpert_api import rigexpert_analyzer

def main():
    velocity_factor = 0.66
    c = 299792458
    cable_velocity = c * velocity_factor

    resonance_frequency = -1

    ra = rigexpert_analyzer()
    ra.cfreq(15e6)
    ra.span(30e6)
    f, r, x = ra.sweep(10)
    f_o = f
    x_o = x

    ra.close()

    for value in range(len(x)):
        if (x[value] * x[value + 1]) < 0:
            resonance_frequency = (f[value] + f[value + 1]) / 2
            break
    print(f"Resonance 1st approximation: {resonance_frequency * 1e6}")

    ra2 = rigexpert_analyzer()
    ra2.cfreq(resonance_frequency * 1e6)
    ra2.span(3e6)
    f, r, x = ra2.sweep(10)

    ra2.close()
    
    for value in range(len(x)):
        if (x[value] * x[value + 1]) < 0:
            resonance_frequency = (f[value] + f[value + 1]) / 2
            break
    print(f"Resonance 2nd approximation: {resonance_frequency * 1e6}")

    ra2 = rigexpert_analyzer()
    ra2.cfreq(resonance_frequency * 1e6)
    ra2.span(0.3e6)
    f, r, x = ra2.sweep(100)

    ra2.close()

    for value in range(len(x)):
        if (x[value] * x[value + 1]) < 0:
            resonance_frequency = (f[value] + f[value + 1]) / 2
            break
    print(f"Final resonance approximation: {resonance_frequency * 1e6}")
    print(f"Cable length or length of fault is: {cable_velocity / (resonance_frequency * 1e6) * (1/4):.2f} m")
    
    # print(f)
    plt.plot(f_o, x_o)
    plt.plot(resonance_frequency, 0, 'ro')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Reactance')
    plt.title(f"Cable Reactance")
    #plt.yticks(np.arange(0, 11, step=1))
    axes = plt.gca()
    #axes.set_ylim([0, 10])
    axes.grid(True)
    #plt.savefig(f"{RADAR}_ant{int(ant):02}.png") 
    plt.show()
    
if __name__ == '__main__':
    main()
