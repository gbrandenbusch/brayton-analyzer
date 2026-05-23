from CoolProp.CoolProp import PropsSI

# Inputs
T1 = 288.15  # ambient T [K]
p1 = 101325  # ambient P [Pa]
pi = 18.0 # pressure ratio
T3 = 1700.0  # turbine inlet T [K]
eta_C = 0.85  # isentropic compressor efficiency
eta_T = 0.90  # isentropic turbine efficiency
fluid = 'Air'

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


print(f"State 1: T={T1:7.1f} K, p={p1/1e5:6.2f} bar")
print(f"State 2: T={T2:7.1f} K, p={p2/1e5:6.2f} bar")
print(f"State 3: T={T3:7.1f} K, p={p3/1e5:6.2f} bar")
print(f"State 4: T={T4:7.1f} K, p={p4/1e5:6.2f} bar")
print()
print(f"w_compressor = {w_C/1e3:6.1f} kJ/kg")
print(f"w_turbine    = {w_T/1e3:6.1f} kJ/kg")
print(f"w_net        = {w_net/1e3:6.1f} kJ/kg")
print(f"q_in         = {q_in/1e3:6.1f} kJ/kg")
print(f"eta_th       = {eta_th*100:6.2f} %")