# utilized ChatGPT
import math


def inches_to_feet(inches):
    """ Convert inches to feet. """
    return inches / 12.0


def microinches_to_feet(microinches):
    """ Convert microinches to feet (1 microinch = 1e-6 inches). """
    return (microinches * 1.0e-6) / 12.0


def gpm_to_ft3_s(gpm):
    """
    Convert gallons per minute (gpm) to cubic feet per second (ft^3/s).
    1 gallon = 0.133681 ft^3
    1 minute = 60 seconds
    """
    return gpm * 0.133681 / 60.0


def compute_re_rr(diameter_in, roughness_microin, flow_gpm, nu=1.217e-5):
    """
    1) Convert diameter (in) -> ft
    2) Convert roughness (microinches) -> ft
    3) Convert flow (gpm) -> ft^3/s
    4) Compute velocity V = Q / (π (D/2)^2)
    5) Compute Re = (V * D) / nu
    6) Compute rr = e / D (relative roughness)

    :param diameter_in: pipe diameter in inches
    :param roughness_microin: pipe roughness in microinches
    :param flow_gpm: flow rate in gallons per minute
    :param nu: kinematic viscosity in ft^2/s (default ~1.217e-5 for water at ~20°C)
    :return: (Re, rr) as floats
    """
    # Convert to feet
    D_ft = inches_to_feet(diameter_in)
    e_ft = microinches_to_feet(roughness_microin)
    Q_ft3_s = gpm_to_ft3_s(flow_gpm)

    # Cross-sectional area
    area = math.pi * (D_ft / 2.0) ** 2
    if area == 0:
        return 0.0, 0.0

    # Velocity (ft/s)
    V_ft_s = Q_ft3_s / area

    # Reynolds number (dimensionless)
    Re = (V_ft_s * D_ft) / nu

    # Relative roughness (dimensionless)
    rr = 0.0 if D_ft == 0 else (e_ft / D_ft)

    return Re, rr
