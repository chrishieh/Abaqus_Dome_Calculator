# Global Parameters

from decimal import Decimal

#------------------------------------------------------------------
# User defined variables

R_mm = 3 # Radius of the circle in meters or millimeters. Either will work as long as the rest of your simulation follows the same units
frequency_n = 4     # Frequency of the geodesic
Dome_calc = True    # Calculate for sphere (=False) or dome (=True)
Icosohedral = False #Set to false to generate spherical dome or true for icosohedral dome
Cylindrical = True
Cut_Point = .5 #Set to a number 0<x<1 to determine point at which the cut is made
#------------------------------------------------------------------
# System variables

nPoint = 1
nEdge = 1
nHub = 1

TINY = Decimal('0.0001')
