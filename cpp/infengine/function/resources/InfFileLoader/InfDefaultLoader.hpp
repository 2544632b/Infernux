#include <function/resources/IMetaCreator.h>
#include <function/resources/InfResource/InfResourceMeta.h>

namespace infengine
{
class InfDefaultTextLoader : public IMetaCreator
{
  public:
    InfDefaultTextLoader();

    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;
};

class InfDefaultBinaryLoader : public IMetaCreator
{
  public:
    InfDefaultBinaryLoader();

    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;

  private:
    /// @brief Get binary file type based on file extension
    /// @param extension The file extension
    /// @return String describing the binary file type
    std::string GetBinaryTypeFromExtension(const std::string &extension) const;
};
} // namespace infengine
