#include "AudioListener.h"
#include "AudioEngine.h"
#include <core/log/InfLog.h>
#include <function/scene/ComponentFactory.h>
#include <function/scene/GameObject.h>

#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace infengine
{

// Register AudioListener with ComponentFactory
INFENGINE_REGISTER_COMPONENT("AudioListener", AudioListener)

void AudioListener::Awake()
{
    AudioEngine::Instance().RegisterListener(this);
    INFLOG_DEBUG("AudioListener registered on GameObject '", GetGameObject() ? GetGameObject()->GetName() : "null",
                 "'");
}

void AudioListener::OnEnable()
{
    AudioEngine::Instance().RegisterListener(this);
}

void AudioListener::OnDisable()
{
    AudioEngine::Instance().UnregisterListener(this);
}

void AudioListener::OnDestroy()
{
    AudioEngine::Instance().UnregisterListener(this);
}

std::string AudioListener::Serialize() const
{
    // AudioListener has no extra properties beyond Component base
    return Component::Serialize();
}

bool AudioListener::Deserialize(const std::string &jsonStr)
{
    return Component::Deserialize(jsonStr);
}

uint64_t AudioListener::GetGameObjectId() const
{
    auto *go = GetGameObject();
    return go ? go->GetID() : 0;
}

} // namespace infengine
