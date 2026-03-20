"""Shared vector coercion utilities."""

from __future__ import annotations

from InfEngine.lib import Vector3 as _Vector3

def coerce_vec3(value) -> _Vector3:
    """Convert a tuple/list/Vector3 to a Vector3, passing through if already one."""
    if isinstance(value, _Vector3):
        return value
    return _Vector3(value[0], value[1], value[2])


def quat_rotate(q, v):
    """Rotate a 3D vector *v* by quaternion *q* (x, y, z, w)."""
    qx, qy, qz, qw = q.x, q.y, q.z, q.w
    vx, vy, vz = v
    tx = 2.0 * (qy * vz - qz * vy)
    ty = 2.0 * (qz * vx - qx * vz)
    tz = 2.0 * (qx * vy - qy * vx)
    return (
        vx + qw * tx + (qy * tz - qz * ty),
        vy + qw * ty + (qz * tx - qx * tz),
        vz + qw * tz + (qx * ty - qy * tx),
    )
