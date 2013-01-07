#**************************************************#
# file   : core/utils.py                           #
# author : Michel Trottier-McDonald                #
# date   : December 2012                           #
# description:                                     #
# A collection of tools to convert between         #
# coordinate systems                               #
#**************************************************#

#############################################################################
#   Copyright 2012-2013 Michel Trottier-McDonald                            #
#                                                                           #
#   This file is part of CDER.                                              #
#                                                                           #
#   CDER is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   CDER is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with CDER.  If not, see <http://www.gnu.org/licenses/>.           #
#############################################################################

## Basic python import
import math

## --------------------------------------- ##
def cart_to_rap(cart_point):
    """
    cart_point is a 3-tuple representing a cartesian point (x, y, z).
    Converts from cartesian to ATLAS pseudo-rapidity coordinates (r, eta, phi),
    where r is the distance from the beam line, not the collision point.
    """

    x = cart_point[0]
    y = cart_point[1]
    z = cart_point[2]

    r     = math.sqrt(x**2 + y**2)
    phi   = math.atan2(y,x)
    theta = math.atan2(r,z)
    eta   = -math.log(math.tan(theta/2.0))

    return (r, eta, phi)



## --------------------------------------- ##
def rap_to_cart(rap_point):
    """
    rap_point is a 3-tuple representing an ATLAS pseudo-rapidity point (r, eta, phi).
    Converts from ATLAS cylindrical to cartesian coordinates (x, y, z),
    r is the distance from the beam line, not the collision point.
    """

    r   = rap_point[0]
    eta = rap_point[1]
    phi = rap_point[2]

    x = r*math.cos(phi)
    y = r*math.sin(phi)

    theta = 2*math.atan(math.exp(-eta))
    z = r/math.tan(theta)

    return (x, y, z)



## --------------------------------------- ##
def cart_to_cyl(cart_point):
    """
    cart_point is a 3-tuple representing a cartesian point (x, y, z).
    Converts from cartesian to ATLAS cylindrical coordinates (r, z, phi),
    where r is the distance from the beam line, not the collision point.
    """

    x = cart_point[0]
    y = cart_point[1]
    z = cart_point[2]

    r   = math.sqrt(x**2 + y**2)
    phi = math.atan2(y,x)

    return (r, z, phi)



## --------------------------------------- ##
def cyl_to_cart(cyl_point):
    """
    cyl_point is a 3-tuple representing an ATLAS cylindrical point (r, z, phi).
    Converts from ATLAS cylindrical to cartesian coordinates (x, y, z),
    r is the distance from the beam line, not the collision point.
    """

    r   = cyl_point[0]
    z   = cyl_point[1]
    phi = cyl_point[2]

    x = r*math.cos(phi)
    y = r*math.sin(phi)

    return (x, y, z)



## --------------------------------------- ##
def z_to_eta(cyl_point):
    """
    cyl_point is a 2-tuple containing radial (r) and longitudinal (z)
    coordinates, what you need to figure out the polar angle w.r.t.
    the transverse plane of the original coordinate system. The resulting
    angle is pseudorapidity.
    """

    r   = cyl_point[0]
    z   = cyl_point[1]

    theta = math.atan2(r,z)
    eta   = -math.log(math.tan(theta/2.0))

    return eta



## --------------------------------------- ##
def eta_to_z(rap_point):
    """
    rap_point is a 2-tuple containing radial (r) and pseudorapidity (eta)
    coordinates, what you need to figure out the longitudinal distance z.
    """

    r   = rap_point[0]
    eta = rap_point[1]

    theta = 2*math.atan(math.exp(-eta))
    z = r/math.tan(theta)

    return z
    


## --------------------------------------- ##
def in2pi(phi):
	"""
	Put all phi values within [0, 2*pi]
    """
    
	while phi >= 2*math.pi : phi -= 2*math.pi
	while phi <  0.0       : phi += 2*math.pi
	return phi



## --------------------------------------- ##
def inabspi(phi):
	"""
	Take all phi values within [-pi, pi]
    """
    
	while phi >= math.pi : phi -= 2*math.pi
	while phi < -math.pi : phi += 2*math.pi
	return phi



## --------------------------------------- ##
def delta_phi(phi1, phi2):
    """
    Find the smaller phi difference between two phi angles
    """
    return min(in2pi(phi1 - phi2), in2pi(phi2 - phi1))



## --------------------------------------- ##
def deg_to_rad(angle):
    """
    converts a degree angle in radians
    """
    return angle * math.pi/180.0



## --------------------------------------- ##
def rad_to_deg(angle):
    """
    converts a radian angle in degrees
    """
    return angle * 180.0/math.pi



## --------------------------------------- ##
def sphy_to_sphz(theta, phi):
    """
    Convert two spherical angles from a spherical coordinate system defined
    around y-axis to two spherical angles in a spherical coordinate system
    defined around the z-axis
    """

    x = math.cos(theta)
    z = math.cos(phi)*math.sin(theta)
    y = math.sin(phi)*math.sin(theta)

    new_phi = math.atan2(y, x)
    new_theta = math.acos(z)

    return new_theta, new_phi
	
    
