#pragma once

#include <core/types/InfFwdType.h>
#include <function/resources/InfResource/InfResourceMeta.h>

#include <memory>
#include <set>
#include <string>

namespace infengine
{

class AssetDatabase;

/// @brief Interface for type-specific asset loading/reloading in AssetRegistry.
///
/// Each ResourceType registers one IAssetLoader implementation.
/// AssetRegistry delegates Load / Reload / ScanDependencies to the loader.
class IAssetLoader
{
  public:
    virtual ~IAssetLoader() = default;

    /// @brief Load an asset from disk.
    /// @return shared_ptr<void> wrapping the concrete asset type.
    virtual std::shared_ptr<void> Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb) = 0;

    /// @brief Reload an already-loaded asset in-place.
    /// @return true on success.
    virtual bool Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                        AssetDatabase *adb) = 0;

    /// @brief Return GUIDs of assets this asset depends on.
    virtual std::set<std::string> ScanDependencies(const std::string &filePath, AssetDatabase *adb) = 0;

    /// @brief Optional: create .meta content for the asset.
    /// Default implementation does nothing. Override in loaders that
    /// need to populate meta beyond what AssetDatabase already provides.
    virtual void CreateMeta(const char * /*content*/, size_t /*contentSize*/, const std::string & /*filePath*/,
                            InfResourceMeta & /*metaData*/)
    {
    }
};

} // namespace infengine
