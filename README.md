# pval

A lightweight package for handling units and physical values in Python.
It is similar to the units and unam packages, without the overhead of user defined fundamental units.

pval only supports the 7 commonly recognized fundamental units:
- length
- mass
- time
- electric current
- absolute temperature
- intensity of light
- quantity of substance

pval also avoids the overhead of attempting to preserve the fundamental units used to create derived or scaled units.
Internally, it uses MKS (meter, kilogram, sec, ampere, Kelvin, candella, and mole).

Unlike units and unam, pval allows the exponents on the fundamental units to be any valid number type, not just integers.
