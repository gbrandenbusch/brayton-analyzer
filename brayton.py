from CoolProp.CoolProp import PropsSI
from numpy import pi


def compute_cycle(pi, T3, eta_C=0.85, eta_T=0.90, T1=288.15, p1=101325, fluid='Air'):
    """
    Parameters
    pi  : float
        Pressure ratio (p2/p1)
    T3 : float
        Turbine inlet temperature [K]
    eta_C : float
        Isentropic compressor efficiency
    eta_T : float
        Isentropic turbine efficiency
    T1 : float
        Ambient temperature [K]
    p1 : float
        Ambient pressure [Pa]
    fluid : str
        CoolProp fluid name
        
    Returns
    dict
        States 1-4 (T, p, h, s) and performance metrics (w_C, w_T, w_net, q_in, eta_th)
    """

    # State 1: compressor inlet
    h1 = PropsSI('H', 'T', T1, 'P', p1, fluid)
    s1 = PropsSI('S', 'T', T1, 'P', p1, fluid)

    # State 2s: compressor outlet
    p2 = pi * p1
    h2s = PropsSI('H', 'P', p2, 'S', s1, fluid)     # isentropic outlet
    h2 = h1 + (h2s - h1) / eta_C                    # actual outlet
    T2 = PropsSI('T', 'P', p2, 'H', h2, fluid)
    s2 = PropsSI('S', 'P', p2, 'H', h2, fluid)

    # State 3: turbine inlet (constant pressure)
    p3 = p2
    h3 = PropsSI('H', 'T', T3, 'P', p3, fluid)
    s3 = PropsSI('S', 'T', T3, 'P', p3, fluid)

    # State 4s: turbine outlet
    p4 = p1
    h4s = PropsSI('H', 'P', p4, 'S', s3, fluid)     # isentropic outlet
    h4 = h3 - eta_T * (h3 - h4s)                    # actual outlet
    T4 = PropsSI('T', 'P', p4, 'H', h4, fluid)
    s4 = PropsSI('S', 'P', p4, 'H', h4, fluid)

    # Performance metrics
    w_C  = h2 - h1  # compressor work
    w_T  = h3 - h4  # turbine work
    w_net = w_T - w_C
    q_in = h3 - h2
    eta_th = w_net / q_in

    return {
        'states': [
            {'T': T1, 'p': p1, 'h': h1, 's': s1},
            {'T': T2, 'p': p2, 'h': h2, 's': s2},
            {'T': T3, 'p': p3, 'h': h3, 's': s3},
            {'T': T4, 'p': p4, 'h': h4, 's': s4}
        ],
        'w_C': w_C,
        'w_T': w_T,
        'w_net': w_net,
        'q_in': q_in,
        'eta_th': eta_th,
    }


if __name__ == "__main__":
    # Demo: reference case
    result = compute_cycle(pi=18.0, T3=1700.0)

    for i, state in enumerate(result['states'], start=1):
        print(f"State {i}: T={state['T']:7.1f} K, p={state['p']/1e5:6.2f} bar")
    
    print()
    print(f"w_compressor = {result['w_C']/1e3:6.1f} kJ/kg")
    print(f"w_turbine    = {result['w_T']/1e3:6.1f} kJ/kg")
    print(f"w_net        = {result['w_net']/1e3:6.1f} kJ/kg")
    print(f"q_in         = {result['q_in']/1e3:6.1f} kJ/kg")
    print(f"eta_th       = {result['eta_th']*100:6.2f} %")