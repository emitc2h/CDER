import math

####################################################
## A collection of tools to convert between ATLAS ##
## and OpenGL coordinates                         ##
####################################################

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


def cyl_to_cart(cyl_point):
    """
    rap_point is a 3-tuple representing an ATLAS cylindrical point (r, z, phi).
    Converts from ATLAS cylindrical to cartesian coordinates (x, y, z),
    r is the distance from the beam line, not the collision point.
    """

    r   = cyl_point[0]
    z   = cyl_point[1]
    phi = cyl_point[2]

    x = r*math.cos(phi)
    y = r*math.sin(phi)

    return (x, y, z)


def in2pi(phi):
	"""
	Take all phi values within 2*pi
    """
    
	while phi >= 2*math.pi : phi -= 2*math.pi
	while phi <  0.0       : phi += 2*math.pi
	return phi


def delta_phi(phi1, phi2):
	return min(in2pi(phi1 - phi2), in2pi(phi2 - phi1))
	
    
