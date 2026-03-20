#pragma once

#include <function/resources/AssetRegistry/AssetRegistry.h>

namespace infengine
{

/**
 * @brief IAssetLoader implementation for shader assets (.vert, .frag).
 *
 * Compiles GLSL source → SPIR-V and produces a ShaderAsset instance
 * containing forward, shadow, and gbuffer pass variants.
 *
 * Key design points:
 *   - Load() reads the shader source, compiles all variants via InfShaderLoader,
 *     and returns a shared_ptr<ShaderAsset>.
 *   - Reload() recompiles and replaces the ShaderAsset data in-place.
 *   - ScanDependencies() returns {} — shaders have no outgoing asset deps.
 */
class ShaderLoader final : public IAssetLoader
{
  public:
    std::shared_ptr<void> Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb) override;

    bool Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                AssetDatabase *adb) override;

    std::set<std::string> ScanDependencies(const std::string &filePath, AssetDatabase *adb) override;
};

} // namespace infengine
