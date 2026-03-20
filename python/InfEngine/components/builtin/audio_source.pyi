from __future__ import annotations

from typing import Any, Optional

from InfEngine.components.builtin_component import BuiltinComponent

class AudioSource(BuiltinComponent):
    """Plays audio clips in the scene."""

    _cpp_type_name: str
    _component_category_: str

    # ---- CppProperty fields as properties ----

    @property
    def track_count(self) -> int:
        """The number of audio tracks on this source."""
        ...
    @track_count.setter
    def track_count(self, value: int) -> None: ...

    @property
    def volume(self) -> float:
        """The overall volume of the audio source."""
        ...
    @volume.setter
    def volume(self, value: float) -> None: ...

    @property
    def pitch(self) -> float:
        """The pitch multiplier of the audio source."""
        ...
    @pitch.setter
    def pitch(self, value: float) -> None: ...

    @property
    def mute(self) -> bool:
        """Whether the audio source is muted."""
        ...
    @mute.setter
    def mute(self, value: bool) -> None: ...

    @property
    def loop(self) -> bool:
        """Whether the audio clip loops when it reaches the end."""
        ...
    @loop.setter
    def loop(self, value: bool) -> None: ...

    @property
    def play_on_awake(self) -> bool:
        """Whether the audio source plays automatically on awake."""
        ...
    @play_on_awake.setter
    def play_on_awake(self, value: bool) -> None: ...

    @property
    def min_distance(self) -> float:
        """The minimum distance for 3D audio attenuation."""
        ...
    @min_distance.setter
    def min_distance(self, value: float) -> None: ...

    @property
    def max_distance(self) -> float:
        """The maximum distance for 3D audio attenuation."""
        ...
    @max_distance.setter
    def max_distance(self, value: float) -> None: ...

    @property
    def one_shot_pool_size(self) -> int:
        """The maximum number of concurrent one-shot sounds."""
        ...
    @one_shot_pool_size.setter
    def one_shot_pool_size(self, value: int) -> None: ...

    @property
    def output_bus(self) -> str:
        """The name of the audio mixer bus to route output to."""
        ...
    @output_bus.setter
    def output_bus(self, value: str) -> None: ...

    # ---- Track management ----

    def set_track_clip(self, track_index: int, clip: Any) -> None:
        """Assign an audio clip to the specified track."""
        ...
    def get_track_clip(self, track_index: int) -> Any:
        """Return the audio clip assigned to the specified track."""
        ...
    def get_track_clip_guid(self, track_index: int) -> str:
        """Return the asset GUID of the clip on the specified track."""
        ...
    def set_track_clip_by_guid(self, track_index: int, guid: str) -> None:
        """Assign an audio clip to a track by its asset GUID."""
        ...
    def set_track_volume(self, track_index: int, volume: float) -> None:
        """Set the volume of the specified track."""
        ...
    def get_track_volume(self, track_index: int) -> float:
        """Return the volume of the specified track."""
        ...

    # ---- Playback control ----

    def play(self, track_index: int = ...) -> None:
        """Start playback on the specified track."""
        ...
    def stop(self, track_index: int = ...) -> None:
        """Stop playback on the specified track."""
        ...
    def play_one_shot(self, clip: Any, volume_scale: float = ...) -> None:
        """Play an audio clip as a one-shot sound."""
        ...
    def stop_one_shots(self) -> None:
        """Stop all currently playing one-shot sounds."""
        ...
    def pause(self, track_index: int = ...) -> None:
        """Pause playback on the specified track."""
        ...
    def un_pause(self, track_index: int = ...) -> None:
        """Resume playback on the specified track."""
        ...
    def stop_all(self) -> None:
        """Stop playback on all tracks and one-shots."""
        ...
    def is_track_playing(self, track_index: int) -> bool:
        """Return whether the specified track is currently playing."""
        ...
    def is_track_paused(self, track_index: int) -> bool:
        """Return whether the specified track is currently paused."""
        ...

    @property
    def is_playing(self) -> bool:
        """Whether any track is currently playing."""
        ...
    @property
    def is_paused(self) -> bool:
        """Whether any track is currently paused."""
        ...

    # ---- Read-only properties ----

    @property
    def game_object_id(self) -> int:
        """The ID of the GameObject this component is attached to."""
        ...

    # ---- Serialization ----

    def serialize(self) -> str:
        """Serialize the component to a JSON string."""
        ...
    def deserialize(self, json_str: str) -> bool:
        """Deserialize the component from a JSON string."""
        ...
