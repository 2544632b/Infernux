@shader_id: lib/vertex_utils

// ============================================================================
// lib/vertex_utils.glsl — Vertex manipulation utilities
//
// Provides: billboard, wind animation, displacement helpers.
// Usage: @import: lib/vertex_utils
// ============================================================================

// Billboard: orient quad to face camera (requires view matrix inverse or camera vectors)
vec3 billboardPosition(vec3 center, vec2 offset, vec3 cameraRight, vec3 cameraUp) {
    return center + cameraRight * offset.x + cameraUp * offset.y;
}

// Axis-locked billboard (rotates around Y axis only)
vec3 billboardAxisY(vec3 center, vec2 offset, vec3 cameraRight) {
    vec3 right = normalize(vec3(cameraRight.x, 0.0, cameraRight.z));
    vec3 up = vec3(0.0, 1.0, 0.0);
    return center + right * offset.x + up * offset.y;
}

// Simple sine-based wind sway
vec3 windSway(vec3 position, float time, float frequency, float amplitude, float phase) {
    float sway = sin(position.x * frequency + time + phase) * amplitude;
    // Scale sway by height (higher vertices sway more)
    sway *= position.y;
    return vec3(sway, 0.0, sway * 0.5);
}

// Vertex displacement along normal
vec3 displaceAlongNormal(vec3 position, vec3 normal, float amount) {
    return position + normal * amount;
}

// Sine wave displacement (for water-like effects)
vec3 sineWaveDisplacement(vec3 position, float time, vec2 direction, float frequency, float amplitude) {
    float phase = dot(position.xz, direction) * frequency + time;
    float height = sin(phase) * amplitude;
    return vec3(0.0, height, 0.0);
}

// Object-space scaling (for pulsing / breathing effects)
vec3 pulseScale(vec3 position, float time, float speed, float minScale, float maxScale) {
    float s = mix(minScale, maxScale, sin(time * speed) * 0.5 + 0.5);
    return position * s;
}
