#pragma once

#include <function/resources/AssetRegistry/AssetRegistry.h>

namespace infengine
{

/**
 * @brief IAssetLoader implementation for 3D model assets (.fbx, .obj, .gltf, …).
 *
 * Uses Assimp to parse the source model file and builds an InfMesh instance
 * containing all submeshes, vertices, and indices ready for GPU upload.
 *
 * The source file (.fbx etc.) is the single source of truth — no intermediate
 * binary format is written.  Import settings (scale, normals, tangents) are
 * read from the .meta file at load time.
 *
 * Key design points:
 *   - Load() produces a new shared_ptr<InfMesh> with combined vertex/index
 *     arrays and one SubMesh per aiMesh in the Assimp scene.
 *   - Reload() replaces the geometry data in-place so all AssetRef holders
 *     see updated data without re-resolving.
 *   - ScanDependencies() returns {} — mesh assets do not reference other
 *     assets (material bindings are on the MeshRenderer, not the mesh).
 */
class MeshLoader final : public IAssetLoader
{
  public:
    std::shared_ptr<void> Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb) override;

    bool Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                AssetDatabase *adb) override;

    std::set<std::string> ScanDependencies(const std::string &filePath, AssetDatabase *adb) override;
};

} // namespace infengine
