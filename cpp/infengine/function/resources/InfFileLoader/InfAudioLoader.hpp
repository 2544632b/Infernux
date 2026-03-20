#pragma once

#include <core/log/InfLog.h>
#include <function/resources/IMetaCreator.h>
#include <function/resources/InfResource/InfResourceMeta.h>

#include <filesystem>

namespace infengine
{

/**
 * @brief File loader for audio resources (.wav).
 *
 * Handles metadata creation and loading for audio files.
 * Actual PCM decoding is done by AudioClip.
 * This loader manages the asset pipeline metadata side.
 */
class InfAudioLoader : public IMetaCreator
{
  public:
    bool LoadMeta(const char * /*content*/, const std::string &filePath, InfResourceMeta &metaData) override
    {
        std::string metaFilePath = InfResourceMeta::GetMetaFilePath(filePath);
        if (metaData.LoadFromFile(metaFilePath)) {
            return true;
        }
        return false;
    }

    void CreateMeta(const char *content, size_t contentSize, const std::string &filePath,
                    InfResourceMeta &metaData) override
    {
        metaData.Init(content, contentSize, filePath, ResourceType::Audio);

        std::filesystem::path path(filePath);
        std::string resourceName = path.stem().string();

        metaData.AddMetadata("resource_name", resourceName);
        metaData.AddMetadata("file_size", static_cast<int>(contentSize));
        metaData.AddMetadata("file_type", std::string("audio"));
        metaData.AddMetadata("extension", path.extension().string());

        // Default audio import settings
        metaData.AddMetadata("force_mono", false);
        metaData.AddMetadata("load_in_background", false);
        metaData.AddMetadata("quality", 1.0f);

        INFLOG_DEBUG("Created audio meta for: ", resourceName, " (", contentSize, " bytes)");
    }
};

} // namespace infengine
