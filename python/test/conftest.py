from __future__ import annotations

import sys
import types

import pytest


class FakeVec3:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __eq__(self, other):
        return isinstance(other, FakeVec3) and (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self):
        return f"FakeVec3({self.x}, {self.y}, {self.z})"


class FakePhysicsBackend:
    def __init__(self):
        self.calls = []
        self.gravity = FakeVec3(0.0, -9.81, 0.0)
        self.layer_pairs = {}
        self.raycast_result = object()
        self.raycast_all_result = [object()]
        self.overlap_sphere_result = [object()]
        self.overlap_box_result = [object()]
        self.sphere_cast_result = object()
        self.box_cast_result = object()

    def _record(self, name, *args):
        self.calls.append((name, args))

    def get_gravity(self):
        self._record("get_gravity")
        return self.gravity

    def set_gravity(self, value):
        self._record("set_gravity", value)
        self.gravity = value

    def raycast(self, *args):
        self._record("raycast", *args)
        return self.raycast_result

    def raycast_all(self, *args):
        self._record("raycast_all", *args)
        return self.raycast_all_result

    def overlap_sphere(self, *args):
        self._record("overlap_sphere", *args)
        return self.overlap_sphere_result

    def overlap_box(self, *args):
        self._record("overlap_box", *args)
        return self.overlap_box_result

    def sphere_cast(self, *args):
        self._record("sphere_cast", *args)
        return self.sphere_cast_result

    def box_cast(self, *args):
        self._record("box_cast", *args)
        return self.box_cast_result

    def ignore_layer_collision(self, layer1, layer2, ignore):
        self._record("ignore_layer_collision", layer1, layer2, ignore)
        self.layer_pairs[(int(layer1), int(layer2))] = bool(ignore)

    def get_ignore_layer_collision(self, layer1, layer2):
        self._record("get_ignore_layer_collision", layer1, layer2)
        return self.layer_pairs.get((int(layer1), int(layer2)), False)


class FakeForceMode:
    Force = "force"
    Acceleration = "acceleration"
    Impulse = "impulse"
    VelocityChange = "velocity_change"


class FakeCppRigidbody:
    def __init__(self):
        self.mass = 1.0
        self.drag = 0.0
        self.angular_drag = 0.05
        self.use_gravity = True
        self.is_kinematic = False
        self.constraints = 0
        self.collision_detection_mode = 0
        self.interpolation = 1
        self.max_angular_velocity = 7.0
        self.max_linear_velocity = 500.0
        self.freeze_rotation = False
        self.velocity = FakeVec3(0.0, 0.0, 0.0)
        self.angular_velocity = FakeVec3(0.0, 0.0, 0.0)
        self.world_center_of_mass = FakeVec3(0.0, 1.0, 0.0)
        self.position = FakeVec3(1.0, 2.0, 3.0)
        self.rotation = (0.0, 0.0, 0.0, 1.0)
        self.calls = []
        self.sleeping = False

    def add_force(self, force, mode):
        self.calls.append(("add_force", force, mode))

    def add_torque(self, torque, mode):
        self.calls.append(("add_torque", torque, mode))

    def add_force_at_position(self, force, position, mode):
        self.calls.append(("add_force_at_position", force, position, mode))

    def move_position(self, position):
        self.calls.append(("move_position", position))

    def move_rotation(self, rotation):
        self.calls.append(("move_rotation", rotation))

    def is_sleeping(self):
        self.calls.append(("is_sleeping",))
        return self.sleeping

    def wake_up(self):
        self.calls.append(("wake_up",))

    def sleep(self):
        self.calls.append(("sleep",))


@pytest.fixture
def fake_infengine_lib(monkeypatch):
    backend = FakePhysicsBackend()
    fake_module = types.ModuleType("InfEngine.lib")
    fake_module.Vector3 = FakeVec3
    fake_module.Physics = backend
    fake_module.ForceMode = FakeForceMode

    import InfEngine

    monkeypatch.setitem(sys.modules, "InfEngine.lib", fake_module)
    monkeypatch.setattr(InfEngine, "lib", fake_module, raising=False)

    # Patch module-level cached imports so physics/rigidbody/coerce see the fakes
    import InfEngine.physics as _phys
    import InfEngine.math.coerce as _coerce
    import InfEngine.components.builtin.rigidbody as _rb
    monkeypatch.setattr(_phys, "_CppPhysics", backend)
    monkeypatch.setattr(_coerce, "_Vector3", FakeVec3)
    monkeypatch.setattr(_rb, "_ForceMode", FakeForceMode)

    return fake_module, backend


@pytest.fixture
def fake_cpp_rigidbody():
    return FakeCppRigidbody()