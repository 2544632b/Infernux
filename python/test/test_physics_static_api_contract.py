from __future__ import annotations

import InfEngine.physics as physics_module
from InfEngine.math.coerce import coerce_vec3


def test_coerce_vec3_converts_tuples(fake_infengine_lib):
    fake_module, _ = fake_infengine_lib
    value = coerce_vec3((1, 2, 3))
    assert isinstance(value, fake_module.Vector3)
    assert (value.x, value.y, value.z) == (1.0, 2.0, 3.0)


def test_coerce_vec3_preserves_existing_vec3(fake_infengine_lib):
    fake_module, _ = fake_infengine_lib
    original = fake_module.Vector3(4, 5, 6)
    assert coerce_vec3(original) is original


def test_gravity_class_property_get_set(fake_infengine_lib):
    fake_module, backend = fake_infengine_lib
    physics_module.Physics.gravity = (3, -2, 1)
    assert isinstance(backend.gravity, fake_module.Vector3)
    assert (backend.gravity.x, backend.gravity.y, backend.gravity.z) == (3.0, -2.0, 1.0)
    gravity = physics_module.Physics.gravity
    assert gravity is backend.gravity


def test_raycast_forwards_arguments(fake_infengine_lib):
    fake_module, backend = fake_infengine_lib
    origin = fake_module.Vector3(1, 2, 3)
    result = physics_module.Physics.raycast(origin, (4, 5, 6), 7.5, 9, False)
    assert result is backend.raycast_result
    name, args = backend.calls[-1]
    assert name == "raycast"
    assert args[0] is origin
    assert isinstance(args[1], fake_module.Vector3)
    assert args[2:] == (7.5, 9, False)


def test_raycast_all_forwards_arguments(fake_infengine_lib):
    fake_module, backend = fake_infengine_lib
    result = physics_module.Physics.raycast_all((1, 1, 1), fake_module.Vector3(0, 1, 0), 8.0, 3, True)
    assert result is backend.raycast_all_result
    name, args = backend.calls[-1]
    assert name == "raycast_all"
    assert isinstance(args[0], fake_module.Vector3)
    assert isinstance(args[1], fake_module.Vector3)
    assert args[2:] == (8.0, 3, True)


def test_overlap_queries_forward_arguments(fake_infengine_lib):
    fake_module, backend = fake_infengine_lib

    sphere_result = physics_module.Physics.overlap_sphere((2, 3, 4), 5.5, 6, False)
    assert sphere_result is backend.overlap_sphere_result
    name, args = backend.calls[-1]
    assert name == "overlap_sphere"
    assert isinstance(args[0], fake_module.Vector3)
    assert args[1:] == (5.5, 6, False)

    box_result = physics_module.Physics.overlap_box(fake_module.Vector3(1, 0, 1), (2, 2, 2), 11, True)
    assert box_result is backend.overlap_box_result
    name, args = backend.calls[-1]
    assert name == "overlap_box"
    assert isinstance(args[0], fake_module.Vector3)
    assert isinstance(args[1], fake_module.Vector3)
    assert args[2:] == (11, True)


def test_shape_casts_forward_arguments(fake_infengine_lib):
    fake_module, backend = fake_infengine_lib

    sphere_hit = physics_module.Physics.sphere_cast((0, 0, 0), 1.25, (0, 0, 1), 9.0, 5, False)
    assert sphere_hit is backend.sphere_cast_result
    name, args = backend.calls[-1]
    assert name == "sphere_cast"
    assert isinstance(args[0], fake_module.Vector3)
    assert isinstance(args[2], fake_module.Vector3)
    assert args[1] == 1.25
    assert args[3:] == (9.0, 5, False)

    box_hit = physics_module.Physics.box_cast((1, 2, 3), (0.5, 1.5, 2.5), fake_module.Vector3(1, 0, 0), 4.0, 2, True)
    assert box_hit is backend.box_cast_result
    name, args = backend.calls[-1]
    assert name == "box_cast"
    assert isinstance(args[0], fake_module.Vector3)
    assert isinstance(args[1], fake_module.Vector3)
    assert isinstance(args[2], fake_module.Vector3)
    assert args[3:] == (4.0, 2, True)


def test_layer_collision_helpers_forward_arguments(fake_infengine_lib):
    _, backend = fake_infengine_lib
    physics_module.Physics.ignore_layer_collision(8, 9, True)
    assert backend.calls[-1] == ("ignore_layer_collision", (8, 9, True))
    assert physics_module.Physics.get_ignore_layer_collision(8, 9) is True
    assert backend.calls[-1] == ("get_ignore_layer_collision", (8, 9))


def test_module_exports_only_physics():
    assert physics_module.__all__ == ["Physics"]