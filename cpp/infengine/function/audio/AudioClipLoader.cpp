#include "AudioClipLoader.h"

#include <core/log/InfLog.h>
#include <function/audio/AudioClip.h>

#include <platform/filesystem/InfPath.h>

#include <filesystem>

namespace infengine
{

// =============================================================================
// Load — decode audio file and create a new AudioClip
// =============================================================================

std::shared_ptr<void> AudioClipLoader::Load(const std::string &filePath, const std::string &guid,
                                            AssetDatabase * /*adb*/)
{
    if (filePath.empty() || guid.empty()) {
        INFLOG_WARN("AudioClipLoader::Load: empty filePath or guid");
        return nullptr;
    }

    auto fsPath = ToFsPath(filePath);
    if (!std::filesystem::exists(fsPath)) {
        INFLOG_ERROR("AudioClipLoader::Load: file not found: ", filePath);
        return nullptr;
    }

    auto clip = std::make_shared<AudioClip>();
    if (!clip->LoadFromFile(filePath)) {
        INFLOG_ERROR("AudioClipLoader::Load: failed to decode: ", filePath);
        return nullptr;
    }

    clip->SetGuid(guid);

    INFLOG_INFO("AudioClipLoader: loaded '", clip->GetName(), "' (GUID: ", guid, ", ", clip->GetDuration(), "s, ",
                clip->GetSampleRate(), " Hz, ", clip->GetChannels(), " ch)");
    return clip;
}

// =============================================================================
// Reload — re-decode audio and replace PCM data in-place
// =============================================================================

bool AudioClipLoader::Reload(std::shared_ptr<void> existing, const std::string &filePath, const std::string &guid,
                             AssetDatabase * /*adb*/)
{
    auto clip = std::static_pointer_cast<AudioClip>(existing);
    if (!clip) {
        INFLOG_WARN("AudioClipLoader::Reload: null existing instance");
        return false;
    }

    // Unload current data and reload from file
    clip->Unload();
    if (!clip->LoadFromFile(filePath)) {
        INFLOG_ERROR("AudioClipLoader::Reload: failed to decode: ", filePath);
        return false;
    }

    // Restore authoritative GUID
    clip->SetGuid(guid);

    INFLOG_INFO("AudioClipLoader: reloaded '", clip->GetName(), "' in-place (GUID: ", guid, ")");
    return true;
}

// =============================================================================
// ScanDependencies — audio clips have no outgoing asset dependencies
// =============================================================================

std::set<std::string> AudioClipLoader::ScanDependencies(const std::string & /*filePath*/, AssetDatabase * /*adb*/)
{
    return {};
}

} // namespace infengine
