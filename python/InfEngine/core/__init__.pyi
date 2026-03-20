"""Type stubs for InfEngine.core."""

from __future__ import annotations

from .material import Material as Material
from .texture import Texture as Texture
from .shader import Shader as Shader
from .audio_clip import AudioClip as AudioClip
from .assets import AssetManager as AssetManager
from .asset_types import (
    TextureImportSettings as TextureImportSettings,
    TextureType as TextureType,
    WrapMode as WrapMode,
    FilterMode as FilterMode,
    ShaderAssetInfo as ShaderAssetInfo,
    FontAssetInfo as FontAssetInfo,
    AudioImportSettings as AudioImportSettings,
    AudioCompressionFormat as AudioCompressionFormat,
    MeshImportSettings as MeshImportSettings,
    asset_category_from_extension as asset_category_from_extension,
    read_meta_file as read_meta_file,
    write_meta_fields as write_meta_fields,
    read_texture_import_settings as read_texture_import_settings,
    write_texture_import_settings as write_texture_import_settings,
    read_audio_import_settings as read_audio_import_settings,
    write_audio_import_settings as write_audio_import_settings,
    read_mesh_import_settings as read_mesh_import_settings,
    write_mesh_import_settings as write_mesh_import_settings,
)
from .asset_ref import (
    TextureRef as TextureRef,
    ShaderRef as ShaderRef,
    AudioClipRef as AudioClipRef,
)

__all__ = [
    "Material",
    "Texture",
    "Shader",
    "AudioClip",
    "AssetManager",
    "TextureImportSettings",
    "TextureType",
    "WrapMode",
    "FilterMode",
    "ShaderAssetInfo",
    "FontAssetInfo",
    "AudioImportSettings",
    "AudioCompressionFormat",
    "MeshImportSettings",
    "TextureRef",
    "ShaderRef",
    "AudioClipRef",
]
