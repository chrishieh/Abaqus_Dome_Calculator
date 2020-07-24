"""The module defines various coordinate transformations and related
functions: transformations between cartesian, cylindrical and spherical
coordinates; rotational matrices; transformations between various
geocentric and heliocentric coordinates (Python wrapper for cxform
library).
"""
# pylint: disable=C0103
import os
import sys
import ctypes
import numpy as np

def cart2sp(x, y, z):
    """Converts data from cartesian coordinates into spherical.

    Args:
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (r, theta, phi) of data in spherical coordinates.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    r = np.sqrt(x**2+y**2+z**2)
    theta = np.arcsin(z/r)
    phi = np.arctan2(y, x)
    if scalar_input:
        return (r.squeeze(), theta.squeeze(), phi.squeeze())
    return (r, theta, phi)

def sp2cart(r, theta, phi):
    """Converts data in spherical coordinates into cartesian.

    Args:
        r (scalar or array_like): R-component of data.
        theta (scalar or array_like): Theta-component of data.
        phi (scalar or array_like): Phi-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    r = np.asarray(r)
    theta = np.asarray(theta)
    phi = np.asarray(phi)
    scalar_input = False
    if r.ndim == 0 and theta.ndim == 0 and phi.ndim == 0:
        r = r[None]
        theta = theta[None]
        phi = phi[None]
        scalar_input = True
    x = r*np.cos(theta)*np.cos(phi)
    y = r*np.cos(theta)*np.sin(phi)
    z = r*np.sin(theta)
    if scalar_input:
        return (x.squeeze(), y.squeeze(), z.squeeze())
    return (x, y, z)

def cart2cyl(x, y, z):
    """Converts data in cartesian coordinates into cylyndrical.

    Args:
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (r, phi, z) of data in cylindrical coordinates.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    r = np.sqrt(x**2+y**2)
    phi = np.arctan2(y, x)
    if scalar_input:
        return (r.squeeze(), phi.squeeze(), z.squeeze())
    return (r, phi, z)

def cyl2cart(r, phi, z):
    """Converts data in cylindrical coordinates into cartesian.

    Args:
        r (scalar or array_like): R-component of data.
        phi (scalar or array_like): Phi-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    r = np.asarray(r)
    phi = np.asarray(phi)
    z = np.asarray(z)
    scalar_input = False
    if r.ndim == 0 and phi.ndim == 0 and z.ndim == 0:
        r = r[None]
        phi = phi[None]
        z = z[None]
        scalar_input = True
    x = r*np.cos(phi)
    y = r*np.sin(phi)
    if scalar_input:
        return (x.squeeze(), y.squeeze(), z.squeeze())
    return (x, y, z)

def mx_rot_x(gamma):
    """Returns rotational matrix for right-handed rotation
    around X axis.

    Args:
        gamma (scalar): Rotation angle around X in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [1, 0, 0],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma), np.cos(gamma)]
    ])

def mx_rot_y(theta):
    """Returns rotational matrix for right-handed rotation
    around Y axis.

    Args:
        theta (scalar): Rotation angle around Y in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def mx_rot_z(phi):
    """Returns rotational matrix for right-handed rotation
    around Z axis.

    Args:
        phi (scalar): Rotation angle around Z in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.matrix([
        [np.cos(phi), -np.sin(phi), 0],
        [np.sin(phi), np.cos(phi), 0],
        [0, 0, 1]
    ])

def mx_rot(theta, phi, gamma):
    """Returns rotational matrix for compound rotation
    around X, Y and Z axes. The order of rotation is X-Y-Z.

    Args:
        theta (scalar): Rotation angle around Y in radians.
        phi (scalar): Rotational angle around in Z radians.
        gamma (scalar): Rotational angle around X in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.dot(
        mx_rot_z(phi),
        np.dot(mx_rot_y(theta), mx_rot_x(gamma))
    )

def mx_rot_reverse(theta, phi, gamma):
    """Returns rotational matrix for compound rotations
    around X, Y and Z axes. The order of rotation is Z-Y-X.

    Args:
        theta (scalar): Rotational angle around Y in radians.
        phi (scalar): Rotational angle around in Z radians.
        gamma (scalar): Rotational angle around X in radians.

    Returns:
        Numpy rotational matrix.
    """
    return np.dot(
        mx_rot_x(gamma),
        np.dot(mx_rot_y(theta), mx_rot_z(phi))
    )

def mx_apply(T, x, y, z):
    """Applies rotation to data using rotational matrix.

    Args:
        T (numpy.matrix): Rotational matrix.
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (x, y, z) of data in cartesian coordinates.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    scalar_input = False
    if x.ndim == 0 and y.ndim == 0 and z.ndim == 0:
        x = x[None]
        y = y[None]
        z = z[None]
        scalar_input = True
    x_ = T[0, 0]*x+T[0, 1]*y+T[0, 2]*z
    y_ = T[1, 0]*x+T[1, 1]*y+T[1, 2]*z
    z_ = T[2, 0]*x+T[2, 1]*y+T[2, 2]*z
    if scalar_input:
        return (x_.squeeze(), y_.squeeze(), z_.squeeze())
    return (x_, y_, z_)

def cxform(cs_from, cs_to, dt, x, y, z):
    """Performs conversion between various geocentric and heliocentric
    coordinate systems.

    Args:
        cs_from (str): Indentifier of the source coordinate system.
            Can be one of 'GEI', 'J2000', 'GEO', 'MAG', 'GSE', 'GSM',
            'SM', 'RTN', 'GSEQ', 'HEE', 'HAE', 'HEEQ'.
        cs_to: Identifier of target coordinate system. Can be one of
            'GEI', 'J2000', 'GEO', 'MAG', 'GSE', 'GSM', 'SM', 'RTN',
            'GSEQ', 'HEE', 'HAE', 'HEEQ'.
        dt (datetime or array_like of datetime): Datetime of the
            conversion.
        x (scalar or array_like): X-component of data.
        y (scalar or array_like): Y-component of data.
        z (scalar or array_like): Z-component of data.

    Returns:
        Tuple (x, y, z) of data in target coordinate system.
    """
    if sys.platform == 'wind32' or sys.platform == 'cygwin':
        libcxform_path = os.path.join(
            os.path.dirname(__file__), 'cxform-c.dll'
        )
    else:
        libcxform_path = os.path.join(
            os.path.dirname(__file__), 'cxform-c.so'
        )
    libcxform = ctypes.CDLL(libcxform_path)
    dt = np.asarray(dt)
    x_from = np.asarray(x)
    y_from = np.asarray(y)
    z_from = np.asarray(z)
    if not dt.shape == x_from.shape == y_from.shape == z_from.shape:
        raise ValueError(
            "x, y, z and dt should be scalars or vectors of the same size"
        )
    scalar_input = False
    if dt.ndim == 0:
        dt = dt[None]
        x_from = x_from[None]
        y_from = y_from[None]
        z_from = z_from[None]
        scalar_input = True
    x_to = np.empty(x_from.shape)
    y_to = np.empty(y_from.shape)
    z_to = np.empty(z_from.shape)
    for i in range(dt.size):
        es = libcxform.date2es(
            ctypes.c_int(dt.flat[i].year),
            ctypes.c_int(dt.flat[i].month),
            ctypes.c_int(dt.flat[i].day),
            ctypes.c_int(dt.flat[i].hour),
            ctypes.c_int(dt.flat[i].minute),
            ctypes.c_int(dt.flat[i].second)
        )
        v_in = np.array(
            [x_from.flat[i], y_from.flat[i], z_from.flat[i]],
            dtype=np.float_
        )
        v_out = np.empty(3, dtype=np.float_)
        libcxform.cxform(
            str.encode(cs_from),
            str.encode(cs_to),
            ctypes.c_double(es),
            v_in.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            v_out.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        )
        x_to.flat[i] = v_out[0]
        y_to.flat[i] = v_out[1]
        z_to.flat[i] = v_out[2]
    if scalar_input:
        return (x_to.squeeze(), y_to.squeeze(), z_to.squeeze())
    return (x_to, y_to, z_to)
