############################################################################
# Smith chart plotting tool v1
#
# Miles Gray Dawkins 03/2025
#
# Function: plot a smith chart without the use of external smith chart 
# or RF libraries. Will allow the use of a compressed smith chart in python
#
# Smith Chart Equation References: http://emlab.uiuc.edu/ece451/appnotes/Smith_chart.pdf
############################################################################


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class smith_chart():
    def __init__():
        # Create a figure and axes
        fig, ax = plt.subplots()

        #set the number of resistance and reactance circles to be displayed
        num_resistance_circles = 11
        num_reactance_circles = 11
        resistances = np.linspace(-5,5,num_resistance_circles)
        reactances = np.linspace(0,5,num_reactance_circles)
        masked = 1

        # Add the resistance linear Axis
        path = [[-1, 0],[1, 0],]
        ax.add_patch(patches.Polygon(path,edgecolor='k', facecolor='none'))

        # Add the resistance circles
        for val in resistances:

            # Highlights the outer boundry of the normal smith chart
            if val==0:
                ax.add_patch(patches.Circle((val/(1+val),0), 1/(1+val), edgecolor='r', facecolor='none'))

            # Shows negative resistances as blue contours
            elif val < 0:
                ax.add_patch(patches.Circle((val/(1+val),0), 1/(1+val), edgecolor='b', facecolor='none'))

            # shows normal resistances as black contours
            else:
                ax.add_patch(patches.Circle((val/(1+val),0), 1/(1+val), edgecolor='k', facecolor='none'))

        #Add the reactance circles
        for val in reactances:
            # must plot both positive and negative reactances
            ax.add_patch(patches.Circle((1,1/val), 1/val, edgecolor='k', facecolor='none'))
            ax.add_patch(patches.Circle((1,1/(-val)), 1/(-val), edgecolor='k', facecolor='none'))

        # Set the aspect ratio to 'equal'
        ax.set_aspect('equal')

        # Set the limits of the plot to accommodate the circle
        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        return ax
