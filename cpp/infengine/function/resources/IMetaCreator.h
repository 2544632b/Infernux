#pragma once

#include <cstddef>
#include <string>

namespace infengine
{

class InfResourceMeta;

/// Lightweight interface for creating / loading .meta sidecar files.
/// Replaces the heavyweight InfFileLoader base class which also carried
/// an unused Load() → InfResource pipeline.
class IMetaCreator
{
  public:
    virtual ~IMetaCreator() = default;

    /// Try to load an existing .meta file.  Return true on success.
    virtual bool LoadMeta(const char *content, const std::string &filePath, InfResourceMeta &metaData) = 0;

    /// Create a brand-new .meta for a file that doesn't have one yet.
    virtual void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                            InfResourceMeta &metaData) = 0;
};

} // namespace infengine
