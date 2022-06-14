# pval

A lightweight package for handling units and physical values in Python.
It is similar to the units and unum packages, without the overhead of user defined fundamental units.

pval only supports the 7 commonly recognized fundamental units:
- length
- mass
- time
- electric charge
- absolute temperature
- intensity of light
- quantity of substance

pval also avoids the overhead of attempting to preserve the fundamental units used to create derived or scaled units.
Internally, it uses MKS (meter, kilogram, sec, coulomb, Kelvin, candela, and mole).

Unlike units and unum, pval allows the exponents on the fundamental units to be any valid number type, not just integers.
