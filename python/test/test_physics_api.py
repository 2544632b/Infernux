from InfEngine.components.builtin import (
    CollisionDetectionMode,
    RigidbodyConstraints,
    RigidbodyInterpolation,
)
from InfEngine.physics import Physics


def test_physics_gravity_is_class_property():
    gravity = Physics.gravity
    assert hasattr(gravity, "x")
    assert hasattr(gravity, "y")
    assert hasattr(gravity, "z")


def test_rigidbody_enums_have_unity_style_values():
    assert int(CollisionDetectionMode.Discrete) == 0
    assert int(CollisionDetectionMode.ContinuousSpeculative) == 3
    assert int(RigidbodyInterpolation.Interpolate) == 1
    assert int(RigidbodyConstraints.FreezeAll) == 126