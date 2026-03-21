#include <function/resources/AssetRegistry/IAssetLoader.h>
#include <function/resources/InfResource/InfResourceMeta.h>

namespace infengine
{
class InfDefaultTextLoader : public IAssetLoader
{
  public:
    InfDefaultTextLoader();

    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;

    std::shared_ptr<void> Load(const std::string & /*filePath*/, const std::string & /*guid*/,
                               AssetDatabase * /*adb*/) override
    {
        return nullptr;
    }
    bool Reload(std::shared_ptr<void> /*existing*/, const std::string & /*filePath*/, const std::string & /*guid*/,
                AssetDatabase * /*adb*/) override
    {
        return false;
    }
    std::set<std::string> ScanDependencies(const std::string & /*filePath*/, AssetDatabase * /*adb*/) override
    {
        return {};
    }
};

class InfDefaultBinaryLoader : public IAssetLoader
{
  public:
    InfDefaultBinaryLoader();

    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;

    std::shared_ptr<void> Load(const std::string & /*filePath*/, const std::string & /*guid*/,
                               AssetDatabase * /*adb*/) override
    {
        return nullptr;
    }
    bool Reload(std::shared_ptr<void> /*existing*/, const std::string & /*filePath*/, const std::string & /*guid*/,
                AssetDatabase * /*adb*/) override
    {
        return false;
    }
    std::set<std::string> ScanDependencies(const std::string & /*filePath*/, AssetDatabase * /*adb*/) override
    {
        return {};
    }

  private:
    /// @brief Get binary file type based on file extension
    /// @param extension The file extension
    /// @return String describing the binary file type
    std::string GetBinaryTypeFromExtension(const std::string &extension) const;
};
} // namespace infengine
