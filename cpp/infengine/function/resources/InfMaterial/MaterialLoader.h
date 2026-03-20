#pragma once

#include <function/resources/AssetRegistry/IAssetLoader.h>

namespace infengine
{

class MaterialLoader final : public IAssetLoader
{
  public:
    std::shared_ptr<void> Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb) override;
    bool Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                AssetDatabase *adb) override;
    std::set<std::string> ScanDependencies(const std::string &filePath, AssetDatabase *adb) override;

  private:
    static void RegisterDependencies(const std::string &materialGuid, const class InfMaterial &mat, AssetDatabase *adb);
};

} // namespace infengine
