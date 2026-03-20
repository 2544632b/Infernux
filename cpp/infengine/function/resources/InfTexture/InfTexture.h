#pragma once

#include <string>

namespace infengine
{

/**
 * @brief Lightweight C++ asset representing a texture's import settings.
 *
 * InfTexture does NOT hold GPU resources (VkImage, VkImageView, etc.).
 * Those remain owned by the renderer's GPU texture cache (InfVkCoreModular).
 *
 * InfTexture is managed by AssetRegistry and provides:
 *   - Cached import settings from the .meta file (sRGB, mipmaps, texture_type)
 *   - GUID / file-path identity
 *   - In-place reload so all holders see updated metadata
 *
 * This decouples metadata reading from the per-frame render path,
 * avoiding repeated .meta file I/O in ResolveTextureForMaterial().
 */
class InfTexture
{
  public:
    InfTexture() = default;

    // ── Identity ────────────────────────────────────────────────────────────

    [[nodiscard]] const std::string &GetGuid() const
    {
        return m_guid;
    }
    void SetGuid(const std::string &guid)
    {
        m_guid = guid;
    }

    [[nodiscard]] const std::string &GetFilePath() const
    {
        return m_filePath;
    }
    void SetFilePath(const std::string &path)
    {
        m_filePath = path;
    }

    [[nodiscard]] const std::string &GetName() const
    {
        return m_name;
    }
    void SetName(const std::string &name)
    {
        m_name = name;
    }

    // ── Import settings (from .meta) ────────────────────────────────────────

    [[nodiscard]] const std::string &GetTextureType() const
    {
        return m_textureType;
    }
    void SetTextureType(const std::string &type)
    {
        m_textureType = type;
    }

    [[nodiscard]] bool IsSrgb() const
    {
        return m_srgb;
    }
    void SetSrgb(bool srgb)
    {
        m_srgb = srgb;
    }

    [[nodiscard]] bool GenerateMipmaps() const
    {
        return m_generateMipmaps;
    }
    void SetGenerateMipmaps(bool gen)
    {
        m_generateMipmaps = gen;
    }

    [[nodiscard]] int GetMaxSize() const
    {
        return m_maxSize;
    }
    void SetMaxSize(int size)
    {
        m_maxSize = size;
    }

    [[nodiscard]] bool IsNormalMapMode() const
    {
        return m_textureType == "normal_map";
    }

    /// Determine whether this texture should use linear format (UNORM).
    /// Solely based on the srgb import setting — no hardcoded texture_type logic.
    [[nodiscard]] bool IsLinear() const
    {
        return !m_srgb;
    }

    /// Load (or refresh) import settings from the .meta file.
    /// @return true if .meta was found and parsed.
    bool LoadImportSettings(const std::string &filePath);

  private:
    std::string m_guid;
    std::string m_filePath;
    std::string m_name;

    // Import settings — defaults match the engine convention (sRGB, mipmaps on)
    std::string m_textureType; // "normal_map", "mask", etc.  Empty = default (color)
    bool m_srgb = true;
    bool m_generateMipmaps = true;
    int m_maxSize = 2048;
};

} // namespace infengine
