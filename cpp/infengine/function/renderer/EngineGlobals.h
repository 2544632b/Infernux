#pragma once

#include <glm/glm.hpp>

namespace infengine
{

/**
 * @brief Engine-wide per-frame globals exposed to all shaders via set 2.
 *
 * Layout matches globals_ubo.glsl (std140).  Each field is a vec4 for
 * alignment simplicity — UE5-style naming conventions.
 *
 * Total size: 8 × vec4 = 128 bytes (well within vkCmdUpdateBuffer's
 * 65536-byte limit and minUniformBufferOffsetAlignment on all GPUs).
 */
struct EngineGlobalsUBO
{
    // ─── Time ───────────────────────────────────────────────────────
    /// x = time since startup (s), y = sin(time), z = cos(time), w = deltaTime
    alignas(16) glm::vec4 time{0.0f};

    /// x = time/20, y = time/4, z = time*2, w = time*3  (UE _Time style)
    alignas(16) glm::vec4 sinTime{0.0f};

    /// x = cos(time/20), y = cos(time/4), z = cos(time*2), w = cos(time*3)
    alignas(16) glm::vec4 cosTime{0.0f};

    // ─── Screen ─────────────────────────────────────────────────────
    /// x = width, y = height, z = 1/width, w = 1/height
    alignas(16) glm::vec4 screenParams{1.0f, 1.0f, 1.0f, 1.0f};

    // ─── Camera ─────────────────────────────────────────────────────
    /// xyz = world-space camera position, w = 1.0
    alignas(16) glm::vec4 worldSpaceCameraPos{0.0f, 0.0f, 0.0f, 1.0f};

    /// x = near, y = far, z = 1/far, w = near/far
    alignas(16) glm::vec4 projectionParams{0.01f, 5000.0f, 0.0002f, 0.000002f};

    /// Linearization helpers for reversed-Z depth buffer.
    /// x = 1 - far/near, y = far/near, z = x/far, w = y/far
    alignas(16) glm::vec4 zBufferParams{1.0f, 0.0f, 0.0f, 0.0f};

    // ─── Frame ──────────────────────────────────────────────────────
    /// x = frame count (float), y = smoothDeltaTime, z = 1/deltaTime, w = unused
    alignas(16) glm::vec4 frameParams{0.0f};
};

static_assert(sizeof(EngineGlobalsUBO) == 128, "EngineGlobalsUBO must be 128 bytes (8 x vec4)");

} // namespace infengine
