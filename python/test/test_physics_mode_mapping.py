from InfEngine.components.builtin import CollisionDetectionMode


def _backend_motion_quality(mode: CollisionDetectionMode, is_kinematic: bool) -> int:
    if mode == CollisionDetectionMode.ContinuousDynamic:
        return 1
    if mode == CollisionDetectionMode.Continuous:
        return 0 if is_kinematic else 1
    return 0


def test_collision_detection_modes_are_not_all_the_same_backend_mapping_for_dynamic():
    assert _backend_motion_quality(CollisionDetectionMode.Discrete, False) == 0
    assert _backend_motion_quality(CollisionDetectionMode.Continuous, False) == 1
    assert _backend_motion_quality(CollisionDetectionMode.ContinuousDynamic, False) == 1
    assert _backend_motion_quality(CollisionDetectionMode.ContinuousSpeculative, False) == 0


def test_collision_detection_modes_have_distinct_kinematic_policy():
    assert _backend_motion_quality(CollisionDetectionMode.Discrete, True) == 0
    assert _backend_motion_quality(CollisionDetectionMode.Continuous, True) == 0
    assert _backend_motion_quality(CollisionDetectionMode.ContinuousDynamic, True) == 1
    assert _backend_motion_quality(CollisionDetectionMode.ContinuousSpeculative, True) == 0