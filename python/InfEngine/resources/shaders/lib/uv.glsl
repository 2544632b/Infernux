@shader_id: lib/uv

// ============================================================================
// lib/uv.glsl — UV manipulation utilities
//
// Provides: tiling, rotation, parallax mapping, triplanar projection.
// Usage: @import: lib/uv
// ============================================================================

// Tile and offset UV
vec2 tilingOffset(vec2 uv, vec2 tiling, vec2 offset) {
    return uv * tiling + offset;
}

// Rotate UV around a center point
vec2 rotateUV(vec2 uv, float angle, vec2 center) {
    float s = sin(angle);
    float c = cos(angle);
    uv -= center;
    return vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c) + center;
}

// Flipbook / sprite sheet UV (row-major, top-left origin)
vec2 flipbookUV(vec2 uv, float cols, float rows, float frame) {
    float totalFrames = cols * rows;
    float idx = mod(floor(frame), totalFrames);
    float col = mod(idx, cols);
    float row = floor(idx / cols);
    vec2 size = vec2(1.0 / cols, 1.0 / rows);
    return vec2(col, row) * size + uv * size;
}

// Simple parallax offset mapping
vec2 parallaxOffset(vec2 uv, vec3 viewDirTangent, float heightMap, float scale) {
    float h = heightMap * scale - scale * 0.5;
    return uv + viewDirTangent.xy / viewDirTangent.z * h;
}

// Triplanar blending weights from world normal
vec3 triplanarWeights(vec3 worldNormal, float sharpness) {
    vec3 w = pow(abs(worldNormal), vec3(sharpness));
    return w / (w.x + w.y + w.z);
}

// Triplanar UV sampling (returns blended color from 3 projections)
vec4 triplanarSample(sampler2D tex, vec3 worldPos, vec3 worldNormal, float tiling, float sharpness) {
    vec3 w = triplanarWeights(worldNormal, sharpness);
    vec4 x = texture(tex, worldPos.yz * tiling);
    vec4 y = texture(tex, worldPos.xz * tiling);
    vec4 z = texture(tex, worldPos.xy * tiling);
    return x * w.x + y * w.y + z * w.z;
}

// Polar UV (radial mapping from center)
vec2 polarUV(vec2 uv, vec2 center) {
    vec2 d = uv - center;
    float r = length(d);
    float angle = atan(d.y, d.x);
    return vec2(angle / 6.28318530718 + 0.5, r);
}
