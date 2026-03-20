#pragma once

#include <function/resources/IMetaCreator.h>
#include <function/resources/InfResource/InfResourceMeta.h>

namespace infengine
{

/**
 * @brief Loader for .mat material files
 *
 * Material files are JSON with the following structure:
 * {
 *   "name": "MaterialName",
 *   "shaders": {
 *     "vertex": "path/to/shader.vert",
 *     "fragment": "path/to/shader.frag"
 *   },
 *   "renderState": { ... },
 *   "properties": { ... }
 * }
 */
class InfMaterialLoader : public IMetaCreator
{
  public:
    bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) override;
    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override;
};

} // namespace infengine
