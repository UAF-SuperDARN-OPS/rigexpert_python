import numpy as np
import matplotlib.pyplot as plt
import csv
import pdb

RADAR = 'mcm'
ant = 1

def main():

    f = np.array([])
    vswr = np.array([])
    
    with open(f"mcm_measurement_1/{RADAR}_ant{int(ant):02}.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        next(csvreader)
        for row in csvreader:
            f = np.append(f,float(row[0]))
            vswr = np.append(vswr,float(row[1]))

    plt.plot(f, vswr )
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('VSWR')
    plt.title(f"Antenna {ant} VSWR")
    plt.yticks(np.arange(0, 11, step=1))
    axes = plt.gca()
    axes.set_ylim([0, 10])
    axes.grid(True)
    plt.savefig(f"read_{RADAR}_ant{int(ant):02}.png") 
    plt.show()
    
if __name__ == '__main__':
    main()
