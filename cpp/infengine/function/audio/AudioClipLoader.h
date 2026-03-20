#pragma once

#include <function/resources/AssetRegistry/IAssetLoader.h>

namespace infengine
{

class AudioClipLoader final : public IAssetLoader
{
  public:
    std::shared_ptr<void> Load(const std::string &filePath, const std::string &guid, AssetDatabase *adb) override;
    bool Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                AssetDatabase *adb) override;
    std::set<std::string> ScanDependencies(const std::string &filePath, AssetDatabase *adb) override;
};

} // namespace infengine
