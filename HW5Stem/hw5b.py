# utilized ChatGPT
# region imports
import hw5a as pta
import myCalcs
import random as rnd
from matplotlib import pyplot as plt
# endregion

# region global variables to store all points
Re_values = []
f_values = []
markers = []
# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2000 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """
    if Re>=4000:
        return pta.ff(Re, rr,CBEQN=True)
    if Re<=2000:
        return pta.ff(Re, rr)
    CBff= pta.ff(Re, rr, CBEQN=True)  #prediction of Colebrook Equation in Transition region
    Lamff= pta.ff(Re, rr)  #prediction of Laminar Equation in Transistion region
    mean=(CBff+Lamff)/2
    sig=0.2*mean
    return rnd.normalvariate(mean, sig)  #use normalvariate to select a number randomly from a normal distribution

def plotAllPoints():
    """
    1) Close any existing figure,
    2) Draw the Moody diagram lines from hw5a.plotMoody(..., doShow=False),
    3) Plot all stored points (Re, f) with their markers,
    4) Finally call plt.show() once.
    """
    plt.close()
    pta.plotMoody(plotPoint=False, pt=(0,0), doShow=False)  # draw the background diagram
    for R, f, mk in zip(Re_values, f_values, markers):
        plt.plot(R, f, marker=mk, markersize=8,
                 markeredgecolor='red', markerfacecolor='none')
    plt.title("Moody Diagram with User Inputs")
    plt.show()

def main():
    while True:
        # Prompt user for diameter or 'q' to quit
        d_str = input("\nEnter pipe diameter (inches) or 'q' to quit: ")
        if d_str.lower() == 'q':
            break

        diameter_in = float(d_str)
        roughness_microin = float(input("Enter pipe roughness (microinches): "))
        flow_gpm = float(input("Enter flow rate (gallons/min): "))

        # 1) Convert to Re, rr using myCalcs
        Re, rr = myCalcs.compute_re_rr(diameter_in, roughness_microin, flow_gpm)

        # 2) Compute friction factor
        f = ffPoint(Re, rr)

        # 3) Decide marker shape: '^' if 2000 <= Re <= 4000, else 'o'
        if 2000 <= Re <= 4000:
            mk = '^'
        else:
            mk = 'o'

        # 4) Append to global lists
        Re_values.append(Re)
        f_values.append(f)
        markers.append(mk)

        # 5) Re-plot the Moody diagram with all points
        plotAllPoints()

    print("\nDone. Exiting the program.")

# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion