# region imports
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
# endregion

# region functions
def ode_system(t, X, *params):
    '''
    The ode system is defined in terms of state variables.
    I have as unknowns:
    x: position of the piston (This is not strictly needed unless I want to know x(t))
    xdot: velocity of the piston
    p1: pressure on right of piston
    p2: pressure on left of the piston
    For initial conditions, we see: x=x0=0, xdot=0, p1=p1_0=p_a, p2=p2_0=p_a
    :param X: The list of state variables.
    :param t: The time for this instance of the function.
    :param params: the list of physical constants for the system.
    :return: The list of derivatives of the state variables.
    '''
    #unpack the parameters
    A, Cd, ps, pa, V, beta, rho, Kvalve, m, y=params

    #state variables
    x    = X[0]
    xdot = X[1]
    p1   = X[2]
    p2   = X[3]


    #conveniently rename the state variables
    x = X[0]  # Piston position
    xdot = X[1]  # Piston velocity
    p1 = X[2]  # Pressure on right of piston
    p2 = X[3]  # Pressure on left of piston

    # calculate derivitives
    """
    Here we perform the derivative calculations for xddot, p1dot, and p2dot.

    We use the relationships from fluid mechanics and Newton's 2nd law:

      1) x'' = (A*(p1 - p2)) / m
         - Newton’s 2nd law states:  m * x'' = A * (p1 - p2).
           Hence dividing both sides by m yields x''.

      2) p1' = ( y*Kvalve*(ps - p1) - rho*A*xdot ) * (beta / (V*rho) )
      3) p2' = ( y*Kvalve*(p2 - pa) - rho*A*xdot ) * (beta / (V*rho) )

    - The terms  y*Kvalve*(ps - p1)  and  y*Kvalve*(p2 - pa)
      represent fluid flow in or out of each chamber.
    - The term  rho*A*xdot  accounts for volume change due to piston movement.
    - Multiplying by  beta/(V*rho)  converts net flow to a rate of change of pressure.
    """

    #use my equations from the assignment
    xddot = (A * (p1 - p2)) / m
    p1dot = (y * Kvalve * (ps - p1) - rho * A * xdot) * (beta / (V * rho))
    p2dot = (y * Kvalve * (p2 - pa) - rho * A * xdot) * (beta / (V * rho))

    #return the list of derivatives of the state variables
    return [xdot, xddot, p1dot, p2dot]

def main():
    #After some trial and error, I found all the action seems to happen in the first 0.02 seconds
    t=np.linspace(0,0.02,200)
    #myargs=(A, Cd, Ps, Pa, V, beta, rho, Kvalve, m, y)
    myargs=(4.909E-4, 0.6, 1.4E7,1.0E5,1.473E-4,2.0E9,850.0,2.0E-5,30, 0.002)
    #because the solution calls for x, xdot, p1 and p2, I make these the state variables X[0], X[1], X[2], X[3]
    #ic=[x=0, xdot=0, p1=pa, p2=pa]
    pa = 1.0E5
    ic = [0, 0, pa, pa]
    #call odeint with ode_system as callback
    sln=solve_ivp(ode_system, (0, 0.02), ic, args=myargs, t_eval=t)

    #unpack result into meaningful names
    xvals = sln.y[0]   # Piston position
    xdot = sln.y[1]  # Piston velocity
    p1 = sln.y[2]    # Pressure on the right side
    p2 = sln.y[3]    # Pressure on the left side

    #plot the result
    plt.subplot(2, 1, 1)
    plt.title('Piston Position and Velocity Over Time')
    plt.plot(t, xvals, 'r-', label='$x$')
    plt.xlabel('Time (s)')
    plt.ylabel('Piston Displacement (m)')
    plt.legend(loc='upper left')

    ax2 = plt.twinx()
    ax2.plot(t, xdot, 'b-', label=r'$\dot{x}$')
    ax2.set_ylabel(r'Piston Velocity $\dot{x}$ (m/s)')
    ax2.legend(loc='lower right')

    plt.subplot(2,1,2)
    plt.title('Pressures $P_1$ and $P_2$ Over Time')
    plt.plot(t, p1, 'b-', label='$P_1$')
    plt.plot(t, p2, 'r-', label='$P_2$')
    plt.legend(loc='lower right')
    plt.xlabel('Time, s')
    plt.ylabel('Pressure (Pascals)')

    plt.tight_layout()
    plt.show()
# endregion

# region function calls
if __name__=="__main__":
    main()
# endregion