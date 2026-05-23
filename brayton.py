from CoolProp.CoolProp import PropsSI

T_ambient = 288.15      # Ambient temperature in Kelvin (15°C)
p_ambient = 101325      # Ambient pressure in Pascals (sea level)

h = PropsSI('H', 'T', T_ambient, 'P', p_ambient, 'Air')
s = PropsSI('S', 'T', T_ambient, 'P', p_ambient, 'Air')

print(f"At T={T_ambient} K, p={p_ambient} Pa:")
print(f" h = {h:.1f} J/kg")
print(f" s = {s:.2f} J/kg*K")