from __future__ import annotations

from InfEngine.components.builtin.rigidbody import (
    CollisionDetectionMode,
    Rigidbody,
    RigidbodyConstraints,
    RigidbodyInterpolation,
)


def test_cpp_properties_round_trip_with_enums(fake_cpp_rigidbody):
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody

    rb.mass = 3.5
    rb.drag = 0.25
    rb.use_gravity = False
    rb.collision_detection_mode = CollisionDetectionMode.ContinuousDynamic
    rb.interpolation = RigidbodyInterpolation.None_

    assert fake_cpp_rigidbody.mass == 3.5
    assert fake_cpp_rigidbody.drag == 0.25
    assert fake_cpp_rigidbody.use_gravity is False
    assert fake_cpp_rigidbody.collision_detection_mode == int(CollisionDetectionMode.ContinuousDynamic)
    assert fake_cpp_rigidbody.interpolation == int(RigidbodyInterpolation.None_)

    fake_cpp_rigidbody.collision_detection_mode = 3
    fake_cpp_rigidbody.interpolation = 1
    assert rb.collision_detection_mode is CollisionDetectionMode.ContinuousSpeculative
    assert rb.interpolation is RigidbodyInterpolation.Interpolate


def test_constraints_helpers_work_as_typed_flags(fake_cpp_rigidbody):
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody

    rb.constraints_flags = RigidbodyConstraints.FreezePositionX | RigidbodyConstraints.FreezeRotationY
    assert rb.has_constraint(RigidbodyConstraints.FreezePositionX)
    assert rb.has_constraint(RigidbodyConstraints.FreezeRotationY)
    assert not rb.has_constraint(RigidbodyConstraints.FreezePositionZ)

    rb.add_constraint(RigidbodyConstraints.FreezeRotationZ)
    assert rb.has_constraint(RigidbodyConstraints.FreezeRotationZ)

    rb.remove_constraint(RigidbodyConstraints.FreezePositionX)
    assert not rb.has_constraint(RigidbodyConstraints.FreezePositionX)


def test_freeze_rotation_passthrough(fake_cpp_rigidbody):
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody

    assert rb.freeze_rotation is False
    rb.freeze_rotation = True
    assert fake_cpp_rigidbody.freeze_rotation is True


def test_velocity_and_angular_velocity_convert_tuples(fake_infengine_lib, fake_cpp_rigidbody):
    fake_module, _ = fake_infengine_lib
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody

    rb.velocity = (1, 2, 3)
    rb.angular_velocity = (4, 5, 6)

    assert isinstance(fake_cpp_rigidbody.velocity, fake_module.Vector3)
    assert isinstance(fake_cpp_rigidbody.angular_velocity, fake_module.Vector3)
    assert (fake_cpp_rigidbody.velocity.x, fake_cpp_rigidbody.velocity.y, fake_cpp_rigidbody.velocity.z) == (1.0, 2.0, 3.0)
    assert (fake_cpp_rigidbody.angular_velocity.x, fake_cpp_rigidbody.angular_velocity.y, fake_cpp_rigidbody.angular_velocity.z) == (4.0, 5.0, 6.0)


def test_force_and_motion_methods_forward_to_cpp(fake_infengine_lib, fake_cpp_rigidbody):
    fake_module, _ = fake_infengine_lib
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody

    rb.add_force((1, 2, 3))
    rb.add_torque((4, 5, 6), fake_module.ForceMode.Impulse)
    rb.add_force_at_position((7, 8, 9), (1, 1, 1), fake_module.ForceMode.Acceleration)
    rb.move_position((3, 2, 1))
    rb.move_rotation((0.0, 0.0, 0.0, 1.0))

    assert fake_cpp_rigidbody.calls[0][0] == "add_force"
    assert fake_cpp_rigidbody.calls[0][2] == fake_module.ForceMode.Force
    assert isinstance(fake_cpp_rigidbody.calls[0][1], fake_module.Vector3)

    assert fake_cpp_rigidbody.calls[1][0] == "add_torque"
    assert fake_cpp_rigidbody.calls[1][2] == fake_module.ForceMode.Impulse

    assert fake_cpp_rigidbody.calls[2][0] == "add_force_at_position"
    assert isinstance(fake_cpp_rigidbody.calls[2][1], fake_module.Vector3)
    assert isinstance(fake_cpp_rigidbody.calls[2][2], fake_module.Vector3)
    assert fake_cpp_rigidbody.calls[2][3] == fake_module.ForceMode.Acceleration

    assert fake_cpp_rigidbody.calls[3][0] == "move_position"
    assert isinstance(fake_cpp_rigidbody.calls[3][1], fake_module.Vector3)
    assert fake_cpp_rigidbody.calls[4] == ("move_rotation", (0.0, 0.0, 0.0, 1.0))


def test_sleep_api_passthrough(fake_cpp_rigidbody):
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody
    fake_cpp_rigidbody.sleeping = True

    assert rb.is_sleeping() is True
    rb.wake_up()
    rb.sleep()

    assert fake_cpp_rigidbody.calls[0] == ("is_sleeping",)
    assert fake_cpp_rigidbody.calls[1] == ("wake_up",)
    assert fake_cpp_rigidbody.calls[2] == ("sleep",)


def test_no_cpp_component_fallbacks_are_safe():
    rb = Rigidbody()
    assert rb.freeze_rotation is False
    assert rb.is_sleeping() is True
    assert rb.rotation == (0.0, 0.0, 0.0, 1.0)
    rb.add_force((1, 2, 3))
    rb.add_torque((1, 2, 3))
    rb.add_force_at_position((1, 2, 3), (0, 0, 0))
    rb.move_position((1, 2, 3))
    rb.move_rotation((0.0, 0.0, 0.0, 1.0))
    rb.wake_up()
    rb.sleep()


def test_read_only_world_info_passthrough(fake_cpp_rigidbody):
    rb = Rigidbody()
    rb._cpp_component = fake_cpp_rigidbody
    assert rb.world_center_of_mass is fake_cpp_rigidbody.world_center_of_mass
    assert rb.position is fake_cpp_rigidbody.position
    assert rb.rotation == fake_cpp_rigidbody.rotation